"""
Data Queries Module for Child Nutrition Dashboard
Contains all SQL queries and data processing functions for the Overview page.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
from .database import get_database

def get_key_metrics() -> Dict[str, any]:
    """
    Get key metrics for the overview page.
    
    Returns:
        Dictionary with metric values
    """
    
    db = get_database()
    
    try:
        # Test connection first
        if not db.test_connection():
            raise Exception("Database connection test failed")
        # Total Children Measured
        total_children_query = """
        SELECT COUNT(DISTINCT BENEFICIARY_ID) as total_children
        FROM CHILD_NUTRITION_DATA 
        WHERE FLAGGED = 0 AND DUPLICATE = 'False'
        """
        total_children_df = db.execute_query(total_children_query)
        total_children = total_children_df.iloc[0]['TOTAL_CHILDREN'] if not total_children_df.empty else 0
        
        # Active Sites
        active_sites_query = """
        SELECT COUNT(DISTINCT SITE) as active_sites
        FROM CHILD_NUTRITION_DATA 
        WHERE FLAGGED = 0 AND DUPLICATE = 'False'
        """
        active_sites_df = db.execute_query(active_sites_query)
        active_sites = active_sites_df.iloc[0]['ACTIVE_SITES'] if not active_sites_df.empty else 0
        
        # Average WHO Z-Score
        avg_zscore_query = """
        SELECT ROUND(AVG(WHO_INDEX), 2) as avg_z_score
        FROM CHILD_NUTRITION_DATA 
        WHERE FLAGGED = 0 AND DUPLICATE = 'False'
        """
        avg_zscore_df = db.execute_query(avg_zscore_query)
        avg_zscore = avg_zscore_df.iloc[0]['AVG_Z_SCORE'] if not avg_zscore_df.empty else 0
        
        # Stunting Reduction (first vs last measurement)
        stunting_reduction_query = """
        WITH first_measurements AS (
            SELECT BENEFICIARY_ID, WHO_INDEX,
                   ROW_NUMBER() OVER (PARTITION BY BENEFICIARY_ID ORDER BY CAPTURE_DATE) as rn
            FROM CHILD_NUTRITION_DATA 
            WHERE FLAGGED = 0 AND DUPLICATE = 'False'
        ),
        last_measurements AS (
            SELECT BENEFICIARY_ID, WHO_INDEX,
                   ROW_NUMBER() OVER (PARTITION BY BENEFICIARY_ID ORDER BY CAPTURE_DATE DESC) as rn
            FROM CHILD_NUTRITION_DATA 
            WHERE FLAGGED = 0 AND DUPLICATE = 'False'
        ),
        stunting_rates AS (
            SELECT 
                AVG(CASE WHEN f.WHO_INDEX < -2 THEN 1.0 ELSE 0.0 END) as first_stunting_rate,
                AVG(CASE WHEN l.WHO_INDEX < -2 THEN 1.0 ELSE 0.0 END) as last_stunting_rate
            FROM first_measurements f
            JOIN last_measurements l ON f.BENEFICIARY_ID = l.BENEFICIARY_ID
            WHERE f.rn = 1 AND l.rn = 1
        )
        SELECT ROUND((first_stunting_rate - last_stunting_rate) * 100, 1) as stunting_reduction
        FROM stunting_rates
        """
        stunting_reduction_df = db.execute_query(stunting_reduction_query)
        stunting_reduction = stunting_reduction_df.iloc[0]['STUNTING_REDUCTION'] if not stunting_reduction_df.empty else 0
        
        return {
            'total_children': int(total_children),
            'active_sites': int(active_sites),
            'avg_zscore': float(avg_zscore) if avg_zscore is not None else 0.0,
            'stunting_reduction': float(stunting_reduction) if stunting_reduction is not None else 0.0
        }
        
    except Exception as e:
        raise Exception(f"Failed to load key metrics from database: {str(e)}")

def get_stunting_category_data() -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Get stunting category progress data for Charts 1 & 2.
    
    Returns:
        Tuple of (percentage_data, count_data) DataFrames
    """
    
    db = get_database()
    
    try:
        # Get stunting category progress data
        query = """
        WITH         first_measurements AS (
            SELECT BENEFICIARY_ID, WHO_INDEX,
                   ROW_NUMBER() OVER (PARTITION BY BENEFICIARY_ID ORDER BY CAPTURE_DATE) as rn
            FROM CHILD_NUTRITION_DATA 
            WHERE FLAGGED = 0 AND DUPLICATE = 'False'
        ),
        last_measurements AS (
            SELECT BENEFICIARY_ID, WHO_INDEX,
                   ROW_NUMBER() OVER (PARTITION BY BENEFICIARY_ID ORDER BY CAPTURE_DATE DESC) as rn
            FROM CHILD_NUTRITION_DATA 
            WHERE FLAGGED = 0 AND DUPLICATE = 'False'
        ),
        category_classification AS (
            SELECT 
                'First Measurement' as period,
                SUM(CASE WHEN WHO_INDEX BETWEEN -2 AND -1 THEN 1 ELSE 0 END) as at_risk,
                SUM(CASE WHEN WHO_INDEX BETWEEN -3 AND -2 THEN 1 ELSE 0 END) as stunted,
                SUM(CASE WHEN WHO_INDEX < -3 THEN 1 ELSE 0 END) as severely_stunted,
                COUNT(*) as total
            FROM first_measurements WHERE rn = 1
            UNION ALL
            SELECT 
                'Last Measurement' as period,
                SUM(CASE WHEN WHO_INDEX BETWEEN -2 AND -1 THEN 1 ELSE 0 END) as at_risk,
                SUM(CASE WHEN WHO_INDEX BETWEEN -3 AND -2 THEN 1 ELSE 0 END) as stunted,
                SUM(CASE WHEN WHO_INDEX < -3 THEN 1 ELSE 0 END) as severely_stunted,
                COUNT(*) as total
            FROM last_measurements WHERE rn = 1
        )
        SELECT * FROM category_classification
        """
        
        df = db.execute_query(query)
        
        if df.empty:
            raise Exception("No stunting category data found in database")
        else:
            # Process real data - convert decimal types to float
            percentage_data = df.copy()
            percentage_data['at_risk'] = (percentage_data['AT_RISK'].astype(float) / percentage_data['TOTAL'].astype(float) * 100).round(1)
            percentage_data['stunted'] = (percentage_data['STUNTED'].astype(float) / percentage_data['TOTAL'].astype(float) * 100).round(1)
            percentage_data['severely_stunted'] = (percentage_data['SEVERELY_STUNTED'].astype(float) / percentage_data['TOTAL'].astype(float) * 100).round(1)
            percentage_data['category'] = percentage_data['PERIOD']
            
            count_data = df.copy()
            count_data['at_risk'] = percentage_data['AT_RISK'].astype(int)
            count_data['stunted'] = percentage_data['STUNTED'].astype(int)
            count_data['severely_stunted'] = percentage_data['SEVERELY_STUNTED'].astype(int)
            count_data['category'] = percentage_data['PERIOD']
            
            # Add target goals
            target_row_percent = pd.DataFrame({
                'category': ['Target Goal'],
                'at_risk': [2.5],
                'stunted': [2.5],
                'severely_stunted': [0.15]
            })
            
            target_row_count = pd.DataFrame({
                'category': ['Target Goal'],
                'at_risk': [143],
                'stunted': [143],
                'severely_stunted': [9]
            })
            
            percentage_data = pd.concat([percentage_data, target_row_percent], ignore_index=True)
            count_data = pd.concat([count_data, target_row_count], ignore_index=True)
        
        return percentage_data, count_data
        
    except Exception as e:
        raise Exception(f"Failed to load stunting category data from database: {str(e)}")

def get_temporal_trends_data() -> pd.DataFrame:
    """
    Get temporal trends data for Chart 3.
    
    Returns:
        DataFrame with temporal trends data
    """
    
    db = get_database()
    
    try:
        query = """
        SELECT 
            DATE_TRUNC('quarter', CAPTURE_DATE) as quarter,
            COUNT(*) as measurement_count,
            AVG(WHO_INDEX) as avg_z_score,
            SUM(CASE WHEN WHO_INDEX < -2 THEN 1 ELSE 0 END) * 100.0 / COUNT(*) as stunting_rate
        FROM CHILD_NUTRITION_DATA 
        WHERE FLAGGED = 0 AND DUPLICATE = 'False'
            AND CAPTURE_DATE >= DATEADD(year, -5, CURRENT_DATE())
        GROUP BY DATE_TRUNC('quarter', CAPTURE_DATE)
        ORDER BY quarter
        """
        
        df = db.execute_query(query)
        
        if df.empty:
            raise Exception("No temporal trends data found in database")
        else:
            # Process real data - convert decimal types to float
            df['period'] = df['QUARTER'].astype(str)
            df['measurements'] = df['MEASUREMENT_COUNT'].astype(int)
            df['avg_z_score'] = df['AVG_Z_SCORE'].astype(float).round(2)
            df['stunting_rate'] = df['STUNTING_RATE'].astype(float).round(1)
            
            return df[['period', 'measurements', 'avg_z_score', 'stunting_rate']]
            
    except Exception as e:
        raise Exception(f"Failed to load temporal trends data from database: {str(e)}")

def get_top_sites_data() -> pd.DataFrame:
    """
    Get top sites data for Chart 4.
    
    Returns:
        DataFrame with top sites data
    """
    
    db = get_database()
    
    try:
        query = """
        SELECT 
            SITE,
            COUNT(DISTINCT BENEFICIARY_ID) as children_count,
            ROUND(COUNT(DISTINCT BENEFICIARY_ID) * 100.0 / SUM(COUNT(DISTINCT BENEFICIARY_ID)) OVER (), 1) as percentage
        FROM CHILD_NUTRITION_DATA 
        WHERE FLAGGED = 0 AND DUPLICATE = 'False'
        GROUP BY SITE
        ORDER BY children_count DESC
        LIMIT 10
        """
        
        df = db.execute_query(query)
        
        if df.empty:
            raise Exception("No top sites data found in database")
        else:
            # Process real data - convert decimal types to float
            df['site'] = df['SITE']
            df['children_count'] = df['CHILDREN_COUNT'].astype(int)
            df['percentage'] = df['PERCENTAGE'].astype(float)
            
            return df[['site', 'children_count', 'percentage']]
            
    except Exception as e:
        raise Exception(f"Failed to load top sites data from database: {str(e)}")

def get_program_distribution_data() -> pd.DataFrame:
    """
    Get program distribution data for Chart 5.
    
    Returns:
        DataFrame with program distribution data
    """
    
    db = get_database()
    
    try:
        query = """
        SELECT 
            SITE_GROUP,
            COUNT(DISTINCT BENEFICIARY_ID) as children_count,
            ROUND(COUNT(DISTINCT BENEFICIARY_ID) * 100.0 / SUM(COUNT(DISTINCT BENEFICIARY_ID)) OVER (), 1) as percentage
        FROM CHILD_NUTRITION_DATA 
        WHERE FLAGGED = 0 AND DUPLICATE = 'False'
        GROUP BY SITE_GROUP
        ORDER BY children_count DESC
        """
        
        df = db.execute_query(query)
        
        if df.empty:
            raise Exception("No program distribution data found in database")
        else:
            # Process real data - convert decimal types to float
            df['site_group'] = df['SITE_GROUP']
            df['percentage'] = df['PERCENTAGE'].astype(float)
            df['children_count'] = df['CHILDREN_COUNT'].astype(int)
            
            return df[['site_group', 'percentage', 'children_count']]
            
    except Exception as e:
        raise Exception(f"Failed to load program distribution data from database: {str(e)}")

def get_z_score_distribution_data() -> pd.DataFrame:
    """
    Get WHO Z-Score distribution data for Chart 6.
    
    Returns:
        DataFrame with z-score distribution data
    """
    
    db = get_database()
    
    try:
        query = """
        WITH z_score_bins AS (
            SELECT 
                FLOOR(WHO_INDEX * 2) / 2 as z_score_bin,
                COUNT(*) as frequency
            FROM CHILD_NUTRITION_DATA 
            WHERE FLAGGED = 0 AND DUPLICATE = 'False'
                AND WHO_INDEX BETWEEN -6 AND 6
            GROUP BY FLOOR(WHO_INDEX * 2) / 2
        )
        SELECT z_score_bin, frequency
        FROM z_score_bins
        ORDER BY z_score_bin
        """
        
        df = db.execute_query(query)
        
        if df.empty:
            raise Exception("No z-score distribution data found in database")
        else:
            # Process real data - convert decimal types to float
            df['z_score_bin'] = df['Z_SCORE_BIN'].astype(float)
            df['frequency'] = df['FREQUENCY'].astype(int)
            
            return df[['z_score_bin', 'frequency']]
            
    except Exception as e:
        raise Exception(f"Failed to load z-score distribution data from database: {str(e)}")
