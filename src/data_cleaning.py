"""
Data cleaning functions for child nutrition measurement data.

This module contains functions to clean and prepare child nutrition data
by removing duplicates, extreme values, missing data, and impossible growth patterns.
"""

import pandas as pd
import numpy as np
from typing import Optional, Tuple
import logging

logger = logging.getLogger(__name__)


def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """
    Remove exact duplicate measurements from the dataset.
    
    This function identifies and removes duplicate records based on key fields:
    - BeneficiaryId: Child identifier
    - DatapointName: Measurement type (Height/BMI)
    - Answer: Measurement value
    - Capture Date: Date of measurement
    - Site: Site location (important for multi-site programs)
    
    The function keeps the first occurrence and removes subsequent duplicates.
    This ensures that the same child can have measurements at different sites
    without being incorrectly identified as duplicates.
    
    Parameters:
    df (DataFrame): Raw data with potential duplicates
    
    Returns:
    DataFrame: Data with duplicates removed
    
    Raises:
    ValueError: If required columns are missing
    TypeError: If data types are incompatible
    """
    if df.empty:
        logger.warning("Input DataFrame is empty")
        return df
    
    # Validate required columns exist
    required_columns = ['BeneficiaryId', 'DatapointName', 'Answer', 'Capture Date', 'Site']
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")
    
    initial_count = len(df)
    logger.info(f"Starting duplicate removal for {initial_count:,} records")
    
    # Handle null values in key fields before duplicate detection
    df_processed = df.copy()
    
    # Log null values in key fields
    null_counts = {}
    for col in required_columns:
        null_count = df_processed[col].isnull().sum()
        if null_count > 0:
            null_counts[col] = null_count
            logger.warning(f"Found {null_count:,} null values in {col}")
    
    if null_counts:
        logger.warning(f"Null values found in key fields: {null_counts}")
    
    # Convert data types to ensure consistent comparison
    try:
        # Ensure BeneficiaryId is numeric for consistent comparison
        df_processed['BeneficiaryId'] = pd.to_numeric(df_processed['BeneficiaryId'], errors='coerce')
        
        # Ensure Answer is numeric for consistent comparison
        df_processed['Answer'] = pd.to_numeric(df_processed['Answer'], errors='coerce')
        
        # Ensure Capture Date is datetime for consistent comparison
        if df_processed['Capture Date'].dtype != 'datetime64[ns]':
            df_processed['Capture Date'] = pd.to_datetime(df_processed['Capture Date'], errors='coerce')
        
        # Ensure DatapointName is string for consistent comparison
        df_processed['DatapointName'] = df_processed['DatapointName'].astype(str)
        
        # Ensure Site is string for consistent comparison
        df_processed['Site'] = df_processed['Site'].astype(str)
        
    except Exception as e:
        logger.error(f"Error converting data types: {str(e)}")
        raise TypeError(f"Data type conversion failed: {str(e)}")
    
    # Remove duplicates based on key fields
    # Keep first occurrence, remove subsequent duplicates
    df_clean = df_processed.drop_duplicates(
        subset=required_columns,
        keep='first'
    )
    
    # Calculate statistics
    removed_count = initial_count - len(df_clean)
    removal_percentage = (removed_count / initial_count * 100) if initial_count > 0 else 0
    
    # Log detailed statistics
    logger.info(f"Duplicate removal completed:")
    logger.info(f"  Initial records: {initial_count:,}")
    logger.info(f"  Final records: {len(df_clean):,}")
    logger.info(f"  Duplicates removed: {removed_count:,} ({removal_percentage:.1f}%)")
    
    # Validate removal percentage is reasonable (<5% expected)
    if removal_percentage > 10:
        logger.warning(f"High duplicate percentage detected: {removal_percentage:.1f}%")
    elif removal_percentage > 5:
        logger.info(f"Moderate duplicate percentage: {removal_percentage:.1f}%")
    else:
        logger.info(f"Low duplicate percentage: {removal_percentage:.1f}%")
    
    # Additional validation: Check for any remaining exact duplicates
    remaining_duplicates = df_clean.duplicated(subset=required_columns).sum()
    if remaining_duplicates > 0:
        logger.error(f"Warning: {remaining_duplicates} duplicates still remain after removal")
    else:
        logger.info("No remaining duplicates detected")
    
    return df_clean


def remove_extreme_values(df: pd.DataFrame) -> pd.DataFrame:
    """
    Remove physiologically impossible measurements from child nutrition data.
    
    This function identifies and removes measurements that are biologically
    impossible for children, ensuring data quality for analysis.
    
    Validation Rules:
    - Height measurements: 40-200 cm (realistic child height range)
    - BMI measurements: 5-50 (realistic BMI range for children)
    - Other measurements: Validated based on measurement type
    
    Parameters:
    df (DataFrame): Data with duplicates removed
    
    Returns:
    DataFrame: Data with physiologically impossible values removed
    
    Raises:
    ValueError: If required columns are missing
    TypeError: If data types are incompatible
    """
    if df.empty:
        logger.warning("Input DataFrame is empty")
        return df
    
    # Validate required columns exist
    required_columns = ['DatapointName', 'Answer']
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")
    
    initial_count = len(df)
    logger.info(f"Starting extreme value removal for {initial_count:,} records")
    
    # Handle null values and data type issues
    df_processed = df.copy()
    
    # Log null values in key fields
    null_counts = {}
    for col in required_columns:
        null_count = df_processed[col].isnull().sum()
        if null_count > 0:
            null_counts[col] = null_count
            logger.warning(f"Found {null_count:,} null values in {col}")
    
    if null_counts:
        logger.warning(f"Null values found in key fields: {null_counts}")
    
    # Convert data types for consistent comparison
    try:
        # Ensure Answer is numeric for comparison
        df_processed['Answer'] = pd.to_numeric(df_processed['Answer'], errors='coerce')
        
        # Ensure DatapointName is string for comparison
        df_processed['DatapointName'] = df_processed['DatapointName'].astype(str)
        
    except Exception as e:
        logger.error(f"Error converting data types: {str(e)}")
        raise TypeError(f"Data type conversion failed: {str(e)}")
    
    # Track removal statistics by measurement type
    removal_stats = {
        'height_removed': 0,
        'bmi_removed': 0,
        'other_removed': 0,
        'total_removed': 0
    }
    
    # Get unique measurement types
    measurement_types = df_processed['DatapointName'].unique()
    logger.info(f"Found measurement types: {list(measurement_types)}")
    
    # Initialize mask for all records to keep
    keep_mask = pd.Series([True] * len(df_processed), index=df_processed.index)
    
    # Remove impossible height measurements (40-200 cm)
    height_mask = (
        (df_processed['DatapointName'] == 'Measure: Height') &
        ((df_processed['Answer'] < 40) | (df_processed['Answer'] > 200))
    )
    height_removed = height_mask.sum()
    removal_stats['height_removed'] = height_removed
    keep_mask = keep_mask & ~height_mask
    
    if height_removed > 0:
        logger.info(f"Height measurements removed: {height_removed:,}")
        # Log examples of removed height measurements
        removed_heights = df_processed[height_mask]
        if len(removed_heights) > 0:
            logger.info("Examples of removed height measurements:")
            for idx, row in removed_heights.head(3).iterrows():
                logger.info(f"  Child {row.get('BeneficiaryId', 'N/A')}: {row['Answer']} cm")
    
    # Remove impossible BMI measurements (5-50)
    bmi_mask = (
        (df_processed['DatapointName'] == 'Measure BMI') &
        ((df_processed['Answer'] < 5) | (df_processed['Answer'] > 50))
    )
    bmi_removed = bmi_mask.sum()
    removal_stats['bmi_removed'] = bmi_removed
    keep_mask = keep_mask & ~bmi_mask
    
    if bmi_removed > 0:
        logger.info(f"BMI measurements removed: {bmi_removed:,}")
        # Log examples of removed BMI measurements
        removed_bmi = df_processed[bmi_mask]
        if len(removed_bmi) > 0:
            logger.info("Examples of removed BMI measurements:")
            for idx, row in removed_bmi.head(3).iterrows():
                logger.info(f"  Child {row.get('BeneficiaryId', 'N/A')}: {row['Answer']} BMI")
    
    # Handle other measurement types with general validation
    other_measurements = df_processed[
        (~df_processed['DatapointName'].isin(['Measure: Height', 'Measure BMI'])) &
        (df_processed['DatapointName'].notna())
    ]
    
    if len(other_measurements) > 0:
        logger.info(f"Found {len(other_measurements):,} other measurement types")
        
        # Apply general validation for other measurements
        # Remove negative values and extremely high values (>1000)
        other_mask = (
            (df_processed['DatapointName'].isin(other_measurements['DatapointName'].unique())) &
            ((df_processed['Answer'] < 0) | (df_processed['Answer'] > 1000))
        )
        other_removed = other_mask.sum()
        removal_stats['other_removed'] = other_removed
        keep_mask = keep_mask & ~other_mask
        
        if other_removed > 0:
            logger.info(f"Other measurements removed: {other_removed:,}")
    
    # Apply the keep mask
    df_clean = df_processed[keep_mask].copy()
    
    # Calculate final statistics
    final_count = len(df_clean)
    total_removed = initial_count - final_count
    removal_percentage = (total_removed / initial_count * 100) if initial_count > 0 else 0
    
    removal_stats['total_removed'] = total_removed
    
    # Log comprehensive statistics
    logger.info(f"Extreme value removal completed:")
    logger.info(f"  Initial records: {initial_count:,}")
    logger.info(f"  Final records: {final_count:,}")
    logger.info(f"  Total removed: {total_removed:,} ({removal_percentage:.1f}%)")
    logger.info(f"  Height measurements removed: {removal_stats['height_removed']:,}")
    logger.info(f"  BMI measurements removed: {removal_stats['bmi_removed']:,}")
    logger.info(f"  Other measurements removed: {removal_stats['other_removed']:,}")
    
    # Validate removal percentage is reasonable (1-3% expected)
    if removal_percentage > 10:
        logger.warning(f"High removal percentage detected: {removal_percentage:.1f}%")
    elif removal_percentage > 5:
        logger.info(f"Moderate removal percentage: {removal_percentage:.1f}%")
    elif removal_percentage > 0:
        logger.info(f"Low removal percentage: {removal_percentage:.1f}%")
    else:
        logger.info("No extreme values found")
    
    # Additional validation: Check for any remaining extreme values
    remaining_extreme = 0
    if 'Measure: Height' in df_clean['DatapointName'].values:
        height_extreme = df_clean[
            (df_clean['DatapointName'] == 'Measure: Height') &
            ((df_clean['Answer'] < 40) | (df_clean['Answer'] > 200))
        ]
        remaining_extreme += len(height_extreme)
    
    if 'Measure BMI' in df_clean['DatapointName'].values:
        bmi_extreme = df_clean[
            (df_clean['DatapointName'] == 'Measure BMI') &
            ((df_clean['Answer'] < 5) | (df_clean['Answer'] > 50))
        ]
        remaining_extreme += len(bmi_extreme)
    
    if remaining_extreme > 0:
        logger.warning(f"Warning: {remaining_extreme} extreme values still remain after removal")
    else:
        logger.info("No remaining extreme values detected")
    
    return df_clean


def remove_missing_critical_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Remove records missing essential fields from child nutrition data.
    
    This function identifies and removes records that are missing critical
    fields required for analysis, ensuring data completeness and quality.
    
    Critical Fields:
    - BeneficiaryId: Child identifier (required for all records)
    - Answer: Measurement value (required for all records)
    - Capture Date: Date of measurement (required for all records)
    - DatapointName: Type of measurement (required for all records)
    
    The function handles various null value representations including:
    - pandas NaN values
    - None values
    - Empty strings
    - Whitespace-only strings
    
    Parameters:
    df (DataFrame): Data with extreme values removed
    
    Returns:
    DataFrame: Data with missing critical data removed
    
    Raises:
    ValueError: If required columns are missing
    TypeError: If data types are incompatible
    """
    if df.empty:
        logger.warning("Input DataFrame is empty")
        return df
    
    # Validate required columns exist
    required_columns = ['BeneficiaryId', 'Answer', 'Capture Date', 'DatapointName']
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")
    
    initial_count = len(df)
    logger.info(f"Starting missing critical data removal for {initial_count:,} records")
    
    # Handle null values and data type issues
    df_processed = df.copy()
    
    # Track removal statistics by field
    removal_stats = {
        'beneficiary_id_missing': 0,
        'answer_missing': 0,
        'capture_date_missing': 0,
        'datapoint_name_missing': 0,
        'total_removed': 0
    }
    
    # Log initial null values in critical fields
    logger.info("📊 INITIAL NULL VALUE ANALYSIS:")
    for col in required_columns:
        null_count = df_processed[col].isnull().sum()
        logger.info(f"  {col}: {null_count:,} null values ({null_count / initial_count * 100:.1f}%)")
    
    # Handle various null value representations
    logger.info("🔍 HANDLING NULL VALUE REPRESENTATIONS:")
    
    # Convert data types for consistent null detection
    try:
        # Ensure BeneficiaryId is numeric for null detection
        df_processed['BeneficiaryId'] = pd.to_numeric(df_processed['BeneficiaryId'], errors='coerce')
        
        # Ensure Answer is numeric for null detection
        df_processed['Answer'] = pd.to_numeric(df_processed['Answer'], errors='coerce')
        
        # Ensure Capture Date is datetime for null detection
        if df_processed['Capture Date'].dtype != 'datetime64[ns]':
            df_processed['Capture Date'] = pd.to_datetime(df_processed['Capture Date'], errors='coerce')
        
        # Ensure DatapointName is string for null detection
        df_processed['DatapointName'] = df_processed['DatapointName'].astype(str)
        
    except Exception as e:
        logger.error(f"Error converting data types: {str(e)}")
        raise TypeError(f"Data type conversion failed: {str(e)}")
    
    # Handle empty strings and whitespace-only strings
    logger.info("🧹 CLEANING EMPTY STRINGS AND WHITESPACE:")
    
    # Convert empty strings and whitespace to NaN
    for col in required_columns:
        if col == 'DatapointName':
            # For string columns, handle empty strings and whitespace
            df_processed[col] = df_processed[col].astype(str)
            df_processed[col] = df_processed[col].str.strip()
            df_processed[col] = df_processed[col].replace('', np.nan)
            df_processed[col] = df_processed[col].replace('nan', np.nan)
            df_processed[col] = df_processed[col].replace('None', np.nan)
            df_processed[col] = df_processed[col].replace('null', np.nan)
            df_processed[col] = df_processed[col].replace('NULL', np.nan)
        else:
            # For numeric/datetime columns, handle string representations of nulls
            if df_processed[col].dtype == 'object':
                df_processed[col] = df_processed[col].astype(str)
                df_processed[col] = df_processed[col].str.strip()
                df_processed[col] = df_processed[col].replace('', np.nan)
                df_processed[col] = df_processed[col].replace('nan', np.nan)
                df_processed[col] = df_processed[col].replace('None', np.nan)
                df_processed[col] = df_processed[col].replace('null', np.nan)
                df_processed[col] = df_processed[col].replace('NULL', np.nan)
    
    # Log null values after cleaning
    logger.info("📊 NULL VALUES AFTER CLEANING:")
    for col in required_columns:
        null_count = df_processed[col].isnull().sum()
        logger.info(f"  {col}: {null_count:,} null values ({null_count / initial_count * 100:.1f}%)")
    
    # Initialize mask for all records to keep
    keep_mask = pd.Series([True] * len(df_processed), index=df_processed.index)
    
    # Remove records missing BeneficiaryId
    beneficiary_id_missing = df_processed['BeneficiaryId'].isnull()
    removal_stats['beneficiary_id_missing'] = beneficiary_id_missing.sum()
    keep_mask = keep_mask & ~beneficiary_id_missing
    
    if removal_stats['beneficiary_id_missing'] > 0:
        logger.info(f"Records missing BeneficiaryId: {removal_stats['beneficiary_id_missing']:,}")
    
    # Remove records missing Answer
    answer_missing = df_processed['Answer'].isnull()
    removal_stats['answer_missing'] = answer_missing.sum()
    keep_mask = keep_mask & ~answer_missing
    
    if removal_stats['answer_missing'] > 0:
        logger.info(f"Records missing Answer: {removal_stats['answer_missing']:,}")
    
    # Remove records missing Capture Date
    capture_date_missing = df_processed['Capture Date'].isnull()
    removal_stats['capture_date_missing'] = capture_date_missing.sum()
    keep_mask = keep_mask & ~capture_date_missing
    
    if removal_stats['capture_date_missing'] > 0:
        logger.info(f"Records missing Capture Date: {removal_stats['capture_date_missing']:,}")
    
    # Remove records missing DatapointName
    datapoint_name_missing = df_processed['DatapointName'].isnull()
    removal_stats['datapoint_name_missing'] = datapoint_name_missing.sum()
    keep_mask = keep_mask & ~datapoint_name_missing
    
    if removal_stats['datapoint_name_missing'] > 0:
        logger.info(f"Records missing DatapointName: {removal_stats['datapoint_name_missing']:,}")
    
    # Apply the keep mask
    df_clean = df_processed[keep_mask].copy()
    
    # Calculate final statistics
    final_count = len(df_clean)
    total_removed = initial_count - final_count
    removal_percentage = (total_removed / initial_count * 100) if initial_count > 0 else 0
    
    removal_stats['total_removed'] = total_removed
    
    # Log comprehensive statistics
    logger.info(f"Missing critical data removal completed:")
    logger.info(f"  Initial records: {initial_count:,}")
    logger.info(f"  Final records: {final_count:,}")
    logger.info(f"  Total removed: {total_removed:,} ({removal_percentage:.1f}%)")
    logger.info(f"  Records missing BeneficiaryId: {removal_stats['beneficiary_id_missing']:,}")
    logger.info(f"  Records missing Answer: {removal_stats['answer_missing']:,}")
    logger.info(f"  Records missing Capture Date: {removal_stats['capture_date_missing']:,}")
    logger.info(f"  Records missing DatapointName: {removal_stats['datapoint_name_missing']:,}")
    
    # Validate removal percentage is reasonable
    if removal_percentage > 50:
        logger.warning(f"High removal percentage detected: {removal_percentage:.1f}%")
    elif removal_percentage > 30:
        logger.info(f"Moderate removal percentage: {removal_percentage:.1f}%")
    elif removal_percentage > 0:
        logger.info(f"Low removal percentage: {removal_percentage:.1f}%")
    else:
        logger.info("No records with missing critical data found")
    
    # Additional validation: Check for any remaining missing critical data
    remaining_missing = 0
    for col in required_columns:
        missing_count = df_clean[col].isnull().sum()
        remaining_missing += missing_count
        if missing_count > 0:
            logger.warning(f"Warning: {missing_count} records still missing {col}")
    
    if remaining_missing > 0:
        logger.warning(f"Warning: {remaining_missing} records still have missing critical data")
    else:
        logger.info("No remaining missing critical data detected")
    
    return df_clean


def fix_data_types(df: pd.DataFrame) -> pd.DataFrame:
    """
    Convert fields to correct data types for child nutrition data.
    
    This function handles comprehensive data type conversion including:
    - Excel serial dates to proper datetime objects
    - Numeric fields to appropriate numeric types
    - Binary fields to 0/1 integers
    - Error handling for conversion failures
    
    Excel Date Conversion:
    - Excel serial numbers (e.g., 44927) converted to datetime
    - Handles Excel date origin (1900-01-01) and leap year bug
    - Preserves timezone information when available
    
    Numeric Field Conversion:
    - Answer: Measurement values converted to float
    - WHO Index: WHO growth standards converted to float
    - BeneficiaryId: Child identifiers converted to integer
    
    Binary Field Conversion:
    - Flagged: Data quality flags converted to 0/1
    - MEASURED: Measurement status converted to 0/1
    
    Parameters:
    df (DataFrame): Data with missing critical data removed
    
    Returns:
    DataFrame: Data with correct data types
    
    Raises:
    ValueError: If required columns are missing
    TypeError: If data type conversion fails
    """
    if df.empty:
        logger.warning("Input DataFrame is empty")
        return df
    
    initial_count = len(df)
    logger.info(f"Starting data type conversion for {initial_count:,} records")
    
    # Track conversion statistics
    conversion_stats = {
        'excel_dates_converted': 0,
        'numeric_fields_converted': 0,
        'binary_fields_converted': 0,
        'conversion_errors': 0
    }
    
    df_clean = df.copy()
    
    # Log initial data types
    logger.info("📊 INITIAL DATA TYPES:")
    for col in df_clean.columns:
        logger.info(f"  {col}: {df_clean[col].dtype}")
    
    # Convert Excel serial dates to proper datetime objects
    logger.info("📅 CONVERTING EXCEL SERIAL DATES:")
    
    date_columns = ['Capture Date', 'CreatedOn']
    for col in date_columns:
        if col in df_clean.columns:
            try:
                # Check if column contains Excel serial numbers
                sample_values = df_clean[col].dropna().head(10)
                if len(sample_values) > 0:
                    # Check if values look like Excel serial numbers (large integers)
                    if sample_values.dtype in ['int64', 'float64'] and sample_values.min() > 1000:
                        logger.info(f"  Converting {col} from Excel serial numbers to datetime")
                        
                        # Convert Excel serial numbers to datetime
                        # Excel date origin is 1900-01-01, but Excel has a leap year bug
                        # So we need to adjust for dates after 1900-02-28
                        def excel_to_datetime(serial):
                            if pd.isna(serial):
                                return pd.NaT
                            # Excel serial number to datetime conversion
                            # Excel counts days since 1900-01-01, but treats 1900 as a leap year
                            # So we need to subtract 2 for dates after 1900-02-28
                            if serial > 59:  # After 1900-02-28
                                serial = serial - 2
                            return pd.Timestamp('1900-01-01') + pd.Timedelta(days=serial-2)
                        
                        df_clean[col] = df_clean[col].apply(excel_to_datetime)
                        conversion_stats['excel_dates_converted'] += 1
                        logger.info(f"  ✅ {col} converted from Excel serial numbers")
                    else:
                        # Regular datetime conversion
                        df_clean[col] = pd.to_datetime(df_clean[col], errors='coerce')
                        logger.info(f"  ✅ {col} converted to datetime")
                else:
                    logger.info(f"  ⚠️ {col} has no valid data to convert")
            except Exception as e:
                logger.error(f"  ❌ Error converting {col}: {str(e)}")
                conversion_stats['conversion_errors'] += 1
    
    # Convert numeric fields to appropriate types
    logger.info("🔢 CONVERTING NUMERIC FIELDS:")
    
    numeric_fields = {
        'Answer': 'float64',
        'WHO Index': 'float64',
        'BeneficiaryId': 'Int64'  # Nullable integer
    }
    
    for field, target_type in numeric_fields.items():
        if field in df_clean.columns:
            try:
                if field == 'BeneficiaryId':
                    # Special handling for BeneficiaryId - convert to nullable integer
                    df_clean[field] = pd.to_numeric(df_clean[field], errors='coerce').astype('Int64')
                else:
                    # Regular numeric conversion
                    df_clean[field] = pd.to_numeric(df_clean[field], errors='coerce').astype(target_type)
                
                conversion_stats['numeric_fields_converted'] += 1
                logger.info(f"  ✅ {field} converted to {target_type}")
            except Exception as e:
                logger.error(f"  ❌ Error converting {field}: {str(e)}")
                conversion_stats['conversion_errors'] += 1
        else:
            logger.info(f"  ⚠️ {field} not found in dataset")
    
    # Convert binary fields to 0/1 integers
    logger.info("🔘 CONVERTING BINARY FIELDS:")
    
    binary_fields = ['Flagged', 'MEASURED']
    for field in binary_fields:
        if field in df_clean.columns:
            try:
                # Convert to numeric first, then to binary
                df_clean[field] = pd.to_numeric(df_clean[field], errors='coerce')
                # Fill NaN values with 0 and convert to int
                df_clean[field] = df_clean[field].fillna(0).astype(int)
                
                conversion_stats['binary_fields_converted'] += 1
                logger.info(f"  ✅ {field} converted to binary (0/1)")
            except Exception as e:
                logger.error(f"  ❌ Error converting {field}: {str(e)}")
                conversion_stats['conversion_errors'] += 1
        else:
            logger.info(f"  ⚠️ {field} not found in dataset")
    
    # Handle other numeric fields that might exist
    logger.info("🔢 CONVERTING OTHER NUMERIC FIELDS:")
    
    other_numeric_fields = ['Score', 'z Score', 'ENTRY NUMBER']
    for field in other_numeric_fields:
        if field in df_clean.columns:
            try:
                df_clean[field] = pd.to_numeric(df_clean[field], errors='coerce')
                logger.info(f"  ✅ {field} converted to numeric")
            except Exception as e:
                logger.error(f"  ❌ Error converting {field}: {str(e)}")
                conversion_stats['conversion_errors'] += 1
    
    # Log final data types
    logger.info("📊 FINAL DATA TYPES:")
    for col in df_clean.columns:
        logger.info(f"  {col}: {df_clean[col].dtype}")
    
    # Log conversion statistics
    logger.info(f"Data type conversion completed:")
    logger.info(f"  Excel dates converted: {conversion_stats['excel_dates_converted']}")
    logger.info(f"  Numeric fields converted: {conversion_stats['numeric_fields_converted']}")
    logger.info(f"  Binary fields converted: {conversion_stats['binary_fields_converted']}")
    logger.info(f"  Conversion errors: {conversion_stats['conversion_errors']}")
    
    # Validate conversion success
    if conversion_stats['conversion_errors'] > 0:
        logger.warning(f"Warning: {conversion_stats['conversion_errors']} conversion errors occurred")
    else:
        logger.info("✅ All data type conversions completed successfully")
    
    # Additional validation: Check for any remaining type issues
    logger.info("🔍 VALIDATING CONVERSION RESULTS:")
    
    # Check for any remaining object types that should be numeric
    for col in df_clean.columns:
        if df_clean[col].dtype == 'object' and col in ['Answer', 'WHO Index', 'BeneficiaryId']:
            logger.warning(f"Warning: {col} is still object type after conversion")
    
    return df_clean
