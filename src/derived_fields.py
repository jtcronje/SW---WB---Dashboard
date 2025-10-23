"""
Derived fields creation for child nutrition measurement data.

This module contains functions to create derived fields for longitudinal
analysis and tracking.
"""

import pandas as pd
import numpy as np
from typing import Union
import logging

logger = logging.getLogger(__name__)


def create_derived_fields(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create time-based tracking fields for monitoring and analysis.
    
    Parameters:
    df (DataFrame): Cleaned data
    
    Returns:
    DataFrame: Data with derived fields added
    """
    # CRITICAL: Must sort by child and date first
    df_sorted = df.sort_values(['BeneficiaryId', 'Capture Date']).copy()
    
    logger.info("Creating derived fields...")
    
    # 1. Days since previous measurement
    df_sorted['days_since_previous_measurement'] = (
        df_sorted.groupby('BeneficiaryId')['Capture Date']
        .diff()
        .dt.days
    )
    
    # 2. Days since first measurement
    df_sorted['days_since_first_measurement'] = (
        df_sorted.groupby('BeneficiaryId')['Capture Date']
        .transform(lambda x: (x - x.min()).dt.days)
    )
    
    # 3. Is first measurement
    df_sorted['is_first_measurement'] = (
        df_sorted.groupby('BeneficiaryId').cumcount() == 0
    ).astype(int)
    
    # 4. Is latest measurement
    df_sorted['is_latest_measurement'] = (
        df_sorted.groupby('BeneficiaryId')['Capture Date']
        .transform('max') == df_sorted['Capture Date']
    ).astype(int)
    
    logger.info("Derived fields created successfully")
    return df_sorted


def validate_derived_fields(df: pd.DataFrame) -> bool:
    """
    Validate that derived fields were created correctly.
    
    Parameters:
    df (DataFrame): Data with derived fields
    
    Returns:
    bool: True if validation passes
    """
    logger.info("Validating derived fields...")
    
    # Check 1: Each child should have exactly one first measurement
    first_measurements = df.groupby('BeneficiaryId')['is_first_measurement'].sum()
    if not all(first_measurements == 1):
        logger.warning("Some children don't have exactly one first measurement!")
        return False
    
    # Check 2: Each child should have at least one latest measurement
    latest_measurements = df.groupby('BeneficiaryId')['is_latest_measurement'].sum()
    if not all(latest_measurements >= 1):
        logger.warning("Some children don't have a latest measurement!")
        return False
    
    # Check 3: days_since_first_measurement should start at 0
    first_records = df[df['is_first_measurement'] == 1]
    if not all(first_records['days_since_first_measurement'] == 0):
        logger.warning("First measurements don't all have days_since_first = 0!")
        return False
    
    logger.info("Derived fields validation passed")
    return True
