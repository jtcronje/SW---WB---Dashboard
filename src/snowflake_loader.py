"""
Snowflake database operations for child nutrition data.

This module contains functions to connect to Snowflake and upload
cleaned data to the cloud data warehouse.
"""

import snowflake.connector
from snowflake.connector.pandas_tools import write_pandas
from dotenv import load_dotenv
import os
import logging
from typing import Optional

logger = logging.getLogger(__name__)


def create_snowflake_connection():
    """
    Create connection to Snowflake.
    
    Returns:
    snowflake.connector.connection: Active connection object
    """
    # Load credentials from .env file
    load_dotenv()
    
    try:
        conn = snowflake.connector.connect(
            account=os.getenv('SNOWFLAKE_ACCOUNT'),
            user=os.getenv('SNOWFLAKE_USER'),
            password=os.getenv('SNOWFLAKE_PASSWORD'),
            warehouse=os.getenv('SNOWFLAKE_WAREHOUSE'),
            database=os.getenv('SNOWFLAKE_DATABASE'),
            schema=os.getenv('SNOWFLAKE_SCHEMA')
        )
        logger.info("Connected to Snowflake successfully")
        return conn
    
    except Exception as e:
        logger.error(f"Failed to connect to Snowflake: {str(e)}")
        raise


def create_snowflake_table(conn):
    """
    Create the nutrition measurements table if it doesn't exist.
    
    Parameters:
    conn: Snowflake connection object
    """
    cursor = conn.cursor()
    
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS CHILD_NUTRITION_MEASUREMENTS (
        BENEFICIARY_ID INTEGER NOT NULL,
        FIRST_NAMES VARCHAR(200),
        LAST_NAME VARCHAR(200),
        HOUSEHOLD_ID INTEGER,
        HOUSEHOLD VARCHAR(300),
        SITE_GROUP VARCHAR(100),
        SITE VARCHAR(200),
        DOMAIN_NAME VARCHAR(100),
        SUBDOMAIN_NAME VARCHAR(100),
        DATAPOINT_NAME VARCHAR(100) NOT NULL,
        ANSWER_INFO VARCHAR(50),
        ANSWER DECIMAL(10,2) NOT NULL,
        RESPONDENT VARCHAR(50),
        WHO_INDEX_TYPE VARCHAR(10),
        WHO_INDEX DECIMAL(5,2),
        SCORE INTEGER,
        FLAGGED INTEGER,
        MEASURED INTEGER,
        DUPLICATE VARCHAR(10),
        ENTRY_NUMBER INTEGER,
        CAPTURE_DATE DATE NOT NULL,
        CREATED_ON TIMESTAMP,
        QUESTION_ID INTEGER,
        DAYS_SINCE_PREVIOUS_MEASUREMENT INTEGER,
        DAYS_SINCE_FIRST_MEASUREMENT INTEGER NOT NULL,
        IS_FIRST_MEASUREMENT INTEGER NOT NULL,
        IS_LATEST_MEASUREMENT INTEGER NOT NULL,
        LOAD_TIMESTAMP TIMESTAMP DEFAULT CURRENT_TIMESTAMP(),
        PRIMARY KEY (BENEFICIARY_ID, CAPTURE_DATE, DATAPOINT_NAME)
    )
    """
    
    try:
        cursor.execute(create_table_sql)
        logger.info("Table created or already exists")
    except Exception as e:
        logger.error(f"Error creating table: {str(e)}")
        raise
    finally:
        cursor.close()


def upload_to_snowflake(df, conn, table_name='CHILD_NUTRITION_MEASUREMENTS'):
    """
    Upload DataFrame to Snowflake table.
    
    Parameters:
    df (DataFrame): Cleaned data to upload
    conn: Snowflake connection object
    table_name (str): Name of target table
    """
    logger.info(f"Uploading {len(df):,} records to Snowflake...")
    
    # Prepare dataframe for Snowflake
    df_upload = prepare_dataframe_for_snowflake(df)
    
    try:
        # Use write_pandas for efficient bulk upload
        success, nchunks, nrows, _ = write_pandas(
            conn=conn,
            df=df_upload,
            table_name=table_name,
            database=os.getenv('SNOWFLAKE_DATABASE'),
            schema=os.getenv('SNOWFLAKE_SCHEMA'),
            auto_create_table=False,
            overwrite=False
        )
        
        if success:
            logger.info(f"Successfully uploaded {nrows:,} rows in {nchunks} chunks")
        else:
            logger.error("Upload failed")
            
    except Exception as e:
        logger.error(f"Error uploading data: {str(e)}")
        raise


def prepare_dataframe_for_snowflake(df):
    """
    Convert DataFrame column names to Snowflake-compatible format.
    
    Parameters:
    df (DataFrame): Data to prepare
    
    Returns:
    DataFrame: Data with Snowflake-compatible column names
    """
    df_upload = df.copy()
    
    # Rename columns to match Snowflake table schema
    column_mapping = {
        'BeneficiaryId': 'BENEFICIARY_ID',
        'FirstNames': 'FIRST_NAMES',
        'LastName': 'LAST_NAME',
        'HouseholdId': 'HOUSEHOLD_ID',
        'Household': 'HOUSEHOLD',
        'Site Group': 'SITE_GROUP',
        'Site': 'SITE',
        'DomainName': 'DOMAIN_NAME',
        'SubDomainName': 'SUBDOMAIN_NAME',
        'DatapointName': 'DATAPOINT_NAME',
        'Answer Info': 'ANSWER_INFO',
        'Answer': 'ANSWER',
        'Respondent': 'RESPONDENT',
        'WHO Index Type': 'WHO_INDEX_TYPE',
        'WHO Index': 'WHO_INDEX',
        'Score': 'SCORE',
        'Flagged': 'FLAGGED',
        'MEASURED': 'MEASURED',
        'DUPLICATE': 'DUPLICATE',
        'ENTRY NUMBER': 'ENTRY_NUMBER',
        'Capture Date': 'CAPTURE_DATE',
        'CreatedOn': 'CREATED_ON',
        'QuestionId': 'QUESTION_ID',
        'days_since_previous_measurement': 'DAYS_SINCE_PREVIOUS_MEASUREMENT',
        'days_since_first_measurement': 'DAYS_SINCE_FIRST_MEASUREMENT',
        'is_first_measurement': 'IS_FIRST_MEASUREMENT',
        'is_latest_measurement': 'IS_LATEST_MEASUREMENT'
    }
    
    df_upload = df_upload.rename(columns=column_mapping)
    
    # Select only columns that exist in Snowflake table
    snowflake_columns = list(column_mapping.values())
    df_upload = df_upload[[col for col in snowflake_columns if col in df_upload.columns]]
    
    return df_upload



