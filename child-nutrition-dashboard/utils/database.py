"""
Database Connection Module for Child Nutrition Dashboard
Handles Snowflake database connectivity with connection pooling and error handling.
"""

import streamlit as st
import snowflake.connector
from snowflake.connector import DictCursor
import pandas as pd
import logging
from typing import Optional, Dict, Any, List
import time
from contextlib import contextmanager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DatabaseConnection:
    """Manages Snowflake database connections with pooling and error handling."""
    
    def __init__(self):
        """Initialize database connection with configuration from Streamlit secrets."""
        self.connection = None
        self.connection_params = self._get_connection_params()
        
    def _get_connection_params(self) -> Dict[str, Any]:
        """Get database connection parameters from Streamlit secrets."""
        try:
            if 'snowflake' not in st.secrets:
                raise ValueError("Snowflake configuration not found in secrets")
            
            return {
                'account': st.secrets['snowflake']['account'],
                'user': st.secrets['snowflake']['user'],
                'password': st.secrets['snowflake']['password'],
                'warehouse': st.secrets['snowflake']['warehouse'],
                'database': st.secrets['snowflake']['database'],
                'schema': st.secrets['snowflake']['schema'],
                'role': st.secrets['snowflake']['role']
            }
        except Exception as e:
            logger.error(f"Failed to get connection parameters: {e}")
            raise
    
    def get_connection(self):
        """Get a database connection from the pool."""
        try:
            if self.connection is None or self.connection.is_closed():
                logger.info("Creating new Snowflake connection")
                logger.info(f"Connection parameters: {self.connection_params}")
                self.connection = snowflake.connector.connect(**self.connection_params)
                logger.info("Successfully connected to Snowflake")
            
            return self.connection
        except Exception as e:
            logger.error(f"Failed to get database connection: {e}")
            logger.error(f"Connection parameters used: {self.connection_params}")
            raise
    
    @contextmanager
    def get_cursor(self):
        """Context manager for database cursor with automatic cleanup."""
        connection = None
        cursor = None
        try:
            connection = self.get_connection()
            cursor = connection.cursor(DictCursor)
            yield cursor
        except Exception as e:
            logger.error(f"Database cursor error: {e}")
            raise
        finally:
            if cursor:
                cursor.close()
    
    def execute_query(self, query: str, params: Optional[Dict] = None) -> pd.DataFrame:
        """
        Execute a parameterized query and return results as DataFrame.
        
        Args:
            query: SQL query string
            params: Optional parameters for the query
            
        Returns:
            pandas.DataFrame: Query results
        """
        try:
            with self.get_cursor() as cursor:
                logger.info(f"Executing query: {query[:100]}...")
                
                if params:
                    cursor.execute(query, params)
                else:
                    cursor.execute(query)
                
                # Fetch results
                results = cursor.fetchall()
                
                if results:
                    # Convert to DataFrame
                    df = pd.DataFrame(results)
                    logger.info(f"Query returned {len(df)} rows")
                    return df
                else:
                    logger.info("Query returned no results")
                    return pd.DataFrame()
                    
        except Exception as e:
            logger.error(f"Query execution failed: {e}")
            raise
    
    def execute_query_with_retry(self, query: str, params: Optional[Dict] = None, 
                               max_retries: int = 3) -> pd.DataFrame:
        """
        Execute query with retry logic for handling transient failures.
        
        Args:
            query: SQL query string
            params: Optional parameters for the query
            max_retries: Maximum number of retry attempts
            
        Returns:
            pandas.DataFrame: Query results
        """
        for attempt in range(max_retries):
            try:
                return self.execute_query(query, params)
            except Exception as e:
                if attempt < max_retries - 1:
                    wait_time = 2 ** attempt  # Exponential backoff
                    logger.warning(f"Query failed (attempt {attempt + 1}), retrying in {wait_time}s: {e}")
                    time.sleep(wait_time)
                else:
                    logger.error(f"Query failed after {max_retries} attempts: {e}")
                    raise
    
    def test_connection(self) -> bool:
        """
        Test database connection with a simple query.
        
        Returns:
            bool: True if connection is successful, False otherwise
        """
        try:
            test_query = "SELECT 1 as test_value"
            result = self.execute_query(test_query)
            return len(result) > 0 and result.iloc[0]['TEST_VALUE'] == 1
        except Exception as e:
            logger.error(f"Connection test failed: {e}")
            return False
    
    def get_table_info(self, table_name: str) -> pd.DataFrame:
        """
        Get information about a specific table.
        
        Args:
            table_name: Name of the table to inspect
            
        Returns:
            pandas.DataFrame: Table information
        """
        query = f"""
        SELECT 
            COLUMN_NAME,
            DATA_TYPE,
            IS_NULLABLE,
            COLUMN_DEFAULT
        FROM INFORMATION_SCHEMA.COLUMNS 
        WHERE TABLE_NAME = UPPER('{table_name}')
        ORDER BY ORDINAL_POSITION
        """
        return self.execute_query(query)
    
    def get_nutrition_data_sample(self, limit: int = 10) -> pd.DataFrame:
        """
        Get a sample of nutrition data for testing.
        
        Args:
            limit: Number of records to return
            
        Returns:
            pandas.DataFrame: Sample nutrition data
        """
        query = f"""
        SELECT 
            BENEFICIARY_ID,
            ANSWER,
            WHO_INDEX,
            CAPTURE_DATE,
            SITE,
            SITE_GROUP,
            FIRST_NAMES,
            LAST_NAME,
            HOUSEHOLD,
            HOUSEHOLD_ID,
            FLAGGED,
            DUPLICATE
        FROM CHILD_NUTRITION_DATA 
        WHERE FLAGGED = 0 AND DUPLICATE = 'False'
        LIMIT {limit}
        """
        return self.execute_query(query)
    
    def close_connection(self):
        """Close the database connection."""
        try:
            if self.connection and not self.connection.is_closed():
                self.connection.close()
                logger.info("Database connection closed")
        except Exception as e:
            logger.error(f"Error closing connection: {e}")
    
    def __del__(self):
        """Destructor to ensure connection is closed."""
        self.close_connection()

# Global database instance
_db_instance = None

def get_database() -> DatabaseConnection:
    """
    Get the global database connection instance.
    
    Returns:
        DatabaseConnection: Database connection instance
    """
    global _db_instance
    if _db_instance is None:
        _db_instance = DatabaseConnection()
    return _db_instance

def close_all_connections():
    """Close all database connections."""
    global _db_instance
    if _db_instance:
        _db_instance.close_connection()
        _db_instance = None

# Convenience functions for common operations
def execute_query(query: str, params: Optional[Dict] = None) -> pd.DataFrame:
    """Execute a query using the global database instance."""
    db = get_database()
    return db.execute_query(query, params)

def execute_query_with_retry(query: str, params: Optional[Dict] = None, 
                            max_retries: int = 3) -> pd.DataFrame:
    """Execute a query with retry logic using the global database instance."""
    db = get_database()
    return db.execute_query_with_retry(query, params, max_retries)

def test_connection() -> bool:
    """Test the database connection."""
    db = get_database()
    return db.test_connection()
