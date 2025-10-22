"""
Snowflake integration module for child nutrition data ETL pipeline.

This module handles:
- Snowflake connection management
- Database and schema creation
- Data upload functionality
- Error handling and retry logic
- Performance optimization
"""

import os
import sys
import time
import logging
import pandas as pd
import numpy as np
from typing import Optional, Dict, Any, List
from contextlib import contextmanager
import snowflake.connector
from snowflake.connector import DictCursor
from snowflake.connector.pandas_tools import write_pandas
import sqlalchemy
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class SnowflakeIntegration:
    """
    Snowflake integration class for child nutrition data ETL pipeline.
    
    This class handles all Snowflake operations including:
    - Connection management
    - Database and schema creation
    - Data upload functionality
    - Error handling and retry logic
    """
    
    def __init__(self):
        """Initialize Snowflake integration with configuration."""
        self.connection_params = {
            'user': os.getenv('SNOWFLAKE_USER', 'JTCronje'),
            'password': os.getenv('SNOWFLAKE_PASSWORD', 'Skollie1308#14'),
            'account': os.getenv('SNOWFLAKE_ACCOUNT', 'vq60567.af-south-1.aws'),
            'warehouse': os.getenv('SNOWFLAKE_WAREHOUSE', 'COMPUTE_WH'),
            'database': 'CHILD_NUTRITION_DB',
            'schema': 'NUTRITION_DATA',
            'role': 'ACCOUNTADMIN'
        }
        
        self.connection = None
        self.engine = None
        
        logger.info("Snowflake integration initialized")
        logger.info(f"Account: {self.connection_params['account']}")
        logger.info(f"Database: {self.connection_params['database']}")
        logger.info(f"Schema: {self.connection_params['schema']}")
    
    @contextmanager
    def get_connection(self):
        """
        Context manager for Snowflake connections with automatic cleanup.
        
        Yields:
            snowflake.connector.SnowflakeConnection: Active connection
        """
        connection = None
        try:
            logger.info("Establishing Snowflake connection...")
            connection = snowflake.connector.connect(
                user=self.connection_params['user'],
                password=self.connection_params['password'],
                account=self.connection_params['account'],
                warehouse=self.connection_params['warehouse'],
                database=self.connection_params['database'],
                schema=self.connection_params['schema'],
                role=self.connection_params['role']
            )
            
            logger.info("✅ Snowflake connection established successfully")
            yield connection
            
        except Exception as e:
            logger.error(f"❌ Snowflake connection failed: {str(e)}")
            raise
        finally:
            if connection:
                try:
                    connection.close()
                    logger.info("Snowflake connection closed")
                except Exception as e:
                    logger.warning(f"Warning: Error closing connection: {str(e)}")
    
    def test_connection(self) -> bool:
        """
        Test Snowflake connection and validate credentials.
        
        Returns:
            bool: True if connection successful, False otherwise
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT CURRENT_VERSION()")
                version = cursor.fetchone()[0]
                logger.info(f"✅ Snowflake connection test successful")
                logger.info(f"Snowflake version: {version}")
                return True
        except Exception as e:
            logger.error(f"❌ Snowflake connection test failed: {str(e)}")
            return False
    
    def create_database_and_schema(self) -> bool:
        """
        Create database and schema in Snowflake.
        
        Returns:
            bool: True if creation successful, False otherwise
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                # Create database
                logger.info("Creating database...")
                cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.connection_params['database']}")
                logger.info(f"✅ Database '{self.connection_params['database']}' created/verified")
                
                # Use the database
                cursor.execute(f"USE DATABASE {self.connection_params['database']}")
                
                # Create schema
                logger.info("Creating schema...")
                cursor.execute(f"CREATE SCHEMA IF NOT EXISTS {self.connection_params['schema']}")
                logger.info(f"✅ Schema '{self.connection_params['schema']}' created/verified")
                
                # Use the schema
                cursor.execute(f"USE SCHEMA {self.connection_params['schema']}")
                
                return True
                
        except Exception as e:
            logger.error(f"❌ Database/schema creation failed: {str(e)}")
            return False
    
    def create_nutrition_data_table(self) -> bool:
        """
        Create the child nutrition data table with appropriate schema.
        
        Returns:
            bool: True if creation successful, False otherwise
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                # Use the database and schema
                cursor.execute(f"USE DATABASE {self.connection_params['database']}")
                cursor.execute(f"USE SCHEMA {self.connection_params['schema']}")
                
                # Create table with comprehensive schema
                create_table_sql = """
                CREATE TABLE IF NOT EXISTS CHILD_NUTRITION_DATA (
                    -- Primary key and identifiers
                    RECORD_ID BIGINT AUTOINCREMENT PRIMARY KEY,
                    BENEFICIARY_ID BIGINT NOT NULL,
                    SITE VARCHAR(255),
                    SITE_GROUP VARCHAR(255),
                    
                    -- Child information
                    FIRST_NAMES VARCHAR(255),
                    NICKNAME VARCHAR(255),
                    LAST_NAME VARCHAR(255),
                    HOUSEHOLD_ID BIGINT,
                    HOUSEHOLD VARCHAR(255),
                    
                    -- Measurement information
                    DATAPOINT_NAME VARCHAR(255) NOT NULL,
                    ANSWER FLOAT NOT NULL,
                    ANSWER_INFO VARCHAR(255),
                    RESPONDENT VARCHAR(255),
                    QUESTION_ID BIGINT,
                    SCORE FLOAT,
                    
                    -- Data quality flags
                    FLAGGED INTEGER DEFAULT 0,
                    MEASURED INTEGER DEFAULT 1,
                    DUPLICATE BOOLEAN DEFAULT FALSE,
                    
                    -- Dates and timestamps
                    CAPTURE_DATE DATE NOT NULL,
                    CREATED_ON TIMESTAMP_NTZ,
                    
                    -- WHO growth standards
                    WHO_INDEX_TYPE VARCHAR(50),
                    WHO_INDEX FLOAT,
                    Z_SCORE FLOAT,
                    
                    -- Additional fields
                    DOMAIN_NAME VARCHAR(255),
                    SUB_DOMAIN_NAME VARCHAR(255),
                    ENTRY_NUMBER INTEGER,
                    
                    -- Metadata
                    LOAD_TIMESTAMP TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
                    DATA_SOURCE VARCHAR(100) DEFAULT 'ETL_PIPELINE'
                )
                """
                
                logger.info("Creating child nutrition data table...")
                cursor.execute(create_table_sql)
                logger.info("✅ Child nutrition data table created successfully")
                
                # Note: Indexes are not supported on regular tables in Snowflake
                # Clustering keys can be set on the table for performance optimization
                logger.info("✅ Table created successfully (indexes not supported on regular tables)")
                
                return True
                
        except Exception as e:
            logger.error(f"❌ Table creation failed: {str(e)}")
            return False
    
    def get_column_mapping(self) -> Dict[str, str]:
        """
        Get column mapping from pandas DataFrame to Snowflake table.
        
        Returns:
            Dict[str, str]: Column mapping dictionary
        """
        return {
            'BeneficiaryId': 'BENEFICIARY_ID',
            'Site': 'SITE',
            'Site Group': 'SITE_GROUP',
            'FirstNames': 'FIRST_NAMES',
            'NickName': 'NICKNAME',
            'LastName': 'LAST_NAME',
            'HouseholdId': 'HOUSEHOLD_ID',
            'Household': 'HOUSEHOLD',
            'DomainName': 'DOMAIN_NAME',
            'SubDomainName': 'SUB_DOMAIN_NAME',
            'DatapointName': 'DATAPOINT_NAME',
            'Answer Info': 'ANSWER_INFO',
            'Answer': 'ANSWER',
            'Respondent': 'RESPONDENT',
            'QuestionId': 'QUESTION_ID',
            'Score': 'SCORE',
            'Flagged': 'FLAGGED',
            'CreatedOn': 'CREATED_ON',
            'Capture Date': 'CAPTURE_DATE',
            'WHO Index Type': 'WHO_INDEX_TYPE',
            'WHO Index': 'WHO_INDEX',
            'z Score': 'Z_SCORE',
            'ENTRY NUMBER': 'ENTRY_NUMBER',
            'MEASURED': 'MEASURED',
            'DUPLICATE': 'DUPLICATE'
        }
    
    def prepare_data_for_upload(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Prepare DataFrame for Snowflake upload.
        
        Args:
            df (pd.DataFrame): Input DataFrame
            
        Returns:
            pd.DataFrame: Prepared DataFrame
        """
        logger.info("Preparing data for Snowflake upload...")
        
        # Create a copy to avoid modifying original
        df_prepared = df.copy()
        
        # Get column mapping
        column_mapping = self.get_column_mapping()
        
        # Remove unwanted columns first
        unwanted_columns = ['Unnamed: 0', 'index']
        for col in unwanted_columns:
            if col in df_prepared.columns:
                df_prepared = df_prepared.drop(columns=[col])
                logger.info(f"Removed unwanted column: {col}")
        
        # Rename columns to match Snowflake schema
        df_prepared = df_prepared.rename(columns=column_mapping)
        
        # Handle data type conversions
        logger.info("Converting data types for Snowflake compatibility...")
        
        # Convert datetime columns
        if 'CAPTURE_DATE' in df_prepared.columns:
            df_prepared['CAPTURE_DATE'] = pd.to_datetime(df_prepared['CAPTURE_DATE'], errors='coerce').dt.date
        
        if 'CREATED_ON' in df_prepared.columns:
            df_prepared['CREATED_ON'] = pd.to_datetime(df_prepared['CREATED_ON'], errors='coerce')
        
        # Convert numeric columns
        numeric_columns = ['BENEFICIARY_ID', 'ANSWER', 'WHO_INDEX', 'SCORE', 'Z_SCORE', 'ENTRY_NUMBER']
        for col in numeric_columns:
            if col in df_prepared.columns:
                df_prepared[col] = pd.to_numeric(df_prepared[col], errors='coerce')
        
        # Convert binary columns
        binary_columns = ['FLAGGED', 'MEASURED']
        for col in binary_columns:
            if col in df_prepared.columns:
                df_prepared[col] = df_prepared[col].fillna(0).astype(int)
        
        # Convert boolean columns
        if 'DUPLICATE' in df_prepared.columns:
            df_prepared['DUPLICATE'] = df_prepared['DUPLICATE'].astype(bool)
        
        # Handle string columns - ensure they're not too long and clean special characters
        string_columns = ['SITE', 'SITE_GROUP', 'FIRST_NAMES', 'NICKNAME', 'LAST_NAME', 
                         'HOUSEHOLD', 'DOMAIN_NAME', 'SUB_DOMAIN_NAME', 'DATAPOINT_NAME', 
                         'ANSWER_INFO', 'RESPONDENT', 'WHO_INDEX_TYPE']
        
        for col in string_columns:
            if col in df_prepared.columns:
                # Convert to string and clean special characters
                df_prepared[col] = df_prepared[col].astype(str)
                
                # Step 1: Replace specific characters with meaningful alternatives
                # Replace & with 'and' to preserve meaning (e.g., "Food & Nutrition" → "Food and Nutrition")
                df_prepared[col] = df_prepared[col].str.replace('&', 'and', regex=False)
                
                # Replace : with space to preserve meaning (e.g., "Measure: Height" → "Measure Height")
                df_prepared[col] = df_prepared[col].str.replace(':', ' ', regex=False)
                
                # Step 2: Clean only truly problematic characters while preserving safe ones
                # Keep letters, numbers, spaces, hyphens, periods, and apostrophes
                df_prepared[col] = df_prepared[col].str.replace(r'[^\w\s\-\.\']', '', regex=True)
                
                # Step 3: Clean control characters that can cause SQL issues
                df_prepared[col] = df_prepared[col].str.replace(r'[\x00-\x1f\x7f-\x9f]', '', regex=True)
                
                # Step 4: Normalize whitespace
                # Replace multiple spaces with single space
                df_prepared[col] = df_prepared[col].str.replace(r'\s+', ' ', regex=True)
                
                # Strip leading/trailing whitespace
                df_prepared[col] = df_prepared[col].str.strip()
                
                # Step 5: Truncate strings to fit Snowflake VARCHAR(255)
                df_prepared[col] = df_prepared[col].str[:255]
                
                # Step 6: Replace empty strings with None
                df_prepared[col] = df_prepared[col].replace('', None)
        
        # Final data cleaning for Snowflake compatibility
        logger.info("🧹 FINAL DATA CLEANING FOR SNOWFLAKE:")
        
        # Replace any remaining NaN values with None for Snowflake compatibility
        df_prepared = df_prepared.where(pd.notnull(df_prepared), None)
        
        # Ensure all column names are valid for Snowflake
        df_prepared.columns = [col.replace(' ', '_').replace('-', '_') for col in df_prepared.columns]
        
        # Remove any rows with all NaN values
        df_prepared = df_prepared.dropna(how='all')
        
        logger.info(f"  ✅ Final data cleaning completed: {len(df_prepared):,} records")
        logger.info(f"✅ Data prepared for upload: {len(df_prepared):,} records")
        return df_prepared
    
    def upload_data(self, df: pd.DataFrame, table_name: str = 'CHILD_NUTRITION_DATA', 
                   chunk_size: int = 10000) -> bool:
        """
        Upload DataFrame to Snowflake table using write_pandas.
        
        Args:
            df (pd.DataFrame): DataFrame to upload
            table_name (str): Target table name
            chunk_size (int): Chunk size for large datasets
            
        Returns:
            bool: True if upload successful, False otherwise
        """
        try:
            # Prepare data for upload
            df_prepared = self.prepare_data_for_upload(df)
            
            logger.info(f"Starting data upload to {table_name}...")
            logger.info(f"Records to upload: {len(df_prepared):,}")
            logger.info(f"Chunk size: {chunk_size:,}")
            
            # Calculate number of chunks
            num_chunks = (len(df_prepared) + chunk_size - 1) // chunk_size
            logger.info(f"Number of chunks: {num_chunks}")
            
            with self.get_connection() as conn:
                # Upload data in chunks
                for i in range(0, len(df_prepared), chunk_size):
                    chunk_df = df_prepared.iloc[i:i + chunk_size]
                    chunk_num = (i // chunk_size) + 1
                    
                    logger.info(f"Uploading chunk {chunk_num}/{num_chunks} ({len(chunk_df):,} records)...")
                    
                    # Use write_pandas for efficient upload
                    try:
                        success, nchunks, nrows, _ = write_pandas(
                            conn=conn,
                            df=chunk_df,
                            table_name=table_name,
                            database=self.connection_params['database'],
                            schema=self.connection_params['schema'],
                            auto_create_table=False,
                            overwrite=False,
                            quote_identifiers=False,
                            on_error='CONTINUE'
                        )
                    except Exception as upload_error:
                        logger.error(f"❌ Upload error for chunk {chunk_num}: {str(upload_error)}")
                        logger.error(f"❌ Error type: {type(upload_error).__name__}")
                        logger.error(f"❌ Error details: {repr(upload_error)}")
                        # Try with a smaller chunk or different approach
                        logger.info(f"Retrying chunk {chunk_num} with error handling...")
                        try:
                            # Reset index to avoid index issues
                            chunk_df_retry = chunk_df.reset_index(drop=True)
                            success, nchunks, nrows, _ = write_pandas(
                                conn=conn,
                                df=chunk_df_retry,
                                table_name=table_name,
                                database=self.connection_params['database'],
                                schema=self.connection_params['schema'],
                                auto_create_table=False,
                                overwrite=False,
                                quote_identifiers=False,
                                on_error='CONTINUE'
                            )
                        except Exception as retry_error:
                            logger.error(f"❌ Retry failed for chunk {chunk_num}: {str(retry_error)}")
                            logger.error(f"❌ Retry error type: {type(retry_error).__name__}")
                            logger.error(f"❌ Retry error details: {repr(retry_error)}")
                            return False
                    
                    if success:
                        logger.info(f"✅ Chunk {chunk_num} uploaded successfully: {nrows:,} rows")
                    else:
                        logger.error(f"❌ Chunk {chunk_num} upload failed")
                        logger.error(f"❌ Success: {success}, nchunks: {nchunks}, nrows: {nrows}")
                        return False
                
                logger.info(f"✅ All data uploaded successfully to {table_name}")
                return True
                
        except Exception as e:
            logger.error(f"❌ Data upload failed: {str(e)}")
            return False
    
    def validate_upload(self, expected_rows: int) -> bool:
        """
        Validate that data was uploaded correctly.
        
        Args:
            expected_rows (int): Expected number of rows
            
        Returns:
            bool: True if validation successful, False otherwise
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                # Count rows in table
                cursor.execute(f"""
                    SELECT COUNT(*) 
                    FROM {self.connection_params['database']}.{self.connection_params['schema']}.CHILD_NUTRITION_DATA
                """)
                
                actual_rows = cursor.fetchone()[0]
                
                logger.info(f"Expected rows: {expected_rows:,}")
                logger.info(f"Actual rows: {actual_rows:,}")
                
                if actual_rows == expected_rows:
                    logger.info("✅ Data upload validation successful")
                    return True
                else:
                    logger.warning(f"⚠️ Row count mismatch: expected {expected_rows:,}, got {actual_rows:,}")
                    return False
                    
        except Exception as e:
            logger.error(f"❌ Upload validation failed: {str(e)}")
            return False
    
    def get_upload_statistics(self) -> Dict[str, Any]:
        """
        Get statistics about uploaded data.
        
        Returns:
            Dict[str, Any]: Upload statistics
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                # Get basic statistics
                cursor.execute(f"""
                    SELECT 
                        COUNT(*) as total_records,
                        COUNT(DISTINCT BENEFICIARY_ID) as unique_children,
                        COUNT(DISTINCT SITE) as unique_sites,
                        MIN(CAPTURE_DATE) as earliest_date,
                        MAX(CAPTURE_DATE) as latest_date,
                        COUNT(DISTINCT DATAPOINT_NAME) as measurement_types
                    FROM {self.connection_params['database']}.{self.connection_params['schema']}.CHILD_NUTRITION_DATA
                """)
                
                stats = cursor.fetchone()
                
                return {
                    'total_records': stats[0],
                    'unique_children': stats[1],
                    'unique_sites': stats[2],
                    'earliest_date': stats[3],
                    'latest_date': stats[4],
                    'measurement_types': stats[5]
                }
                
        except Exception as e:
            logger.error(f"❌ Failed to get upload statistics: {str(e)}")
            return {}


def main():
    """Main function for testing Snowflake integration."""
    logger.info("🚀 TESTING SNOWFLAKE INTEGRATION")
    logger.info("============================================================")
    
    try:
        # Initialize Snowflake integration
        sf = SnowflakeIntegration()
        
        # Test connection
        logger.info("Testing Snowflake connection...")
        if not sf.test_connection():
            logger.error("❌ Connection test failed")
            return False
        
        # Create database and schema
        logger.info("Creating database and schema...")
        if not sf.create_database_and_schema():
            logger.error("❌ Database/schema creation failed")
            return False
        
        # Create table
        logger.info("Creating child nutrition data table...")
        if not sf.create_nutrition_data_table():
            logger.error("❌ Table creation failed")
            return False
        
        logger.info("✅ Snowflake integration setup completed successfully!")
        return True
        
    except Exception as e:
        logger.error(f"❌ Snowflake integration failed: {str(e)}")
        return False


if __name__ == "__main__":
    main()
