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

# ============================================================================
# LOCATION ANALYSIS PAGE QUERIES
# ============================================================================

def get_available_sites() -> pd.DataFrame:
    """
    Get all available sites for location dropdown.
    
    Returns:
        DataFrame with site information
    """
    
    db = get_database()
    
    try:
        query = """
        SELECT DISTINCT 
            SITE,
            COUNT(DISTINCT BENEFICIARY_ID) as child_count
        FROM CHILD_NUTRITION_DATA 
        WHERE FLAGGED = 0 AND DUPLICATE = 'False'
        GROUP BY SITE
        ORDER BY SITE
        """
        
        df = db.execute_query(query)
        
        if df.empty:
            raise Exception("No sites found in database")
        else:
            # Process real data
            df['site'] = df['SITE']
            df['child_count'] = df['CHILD_COUNT'].astype(int)
            
            return df[['site', 'child_count']]
            
    except Exception as e:
        raise Exception(f"Failed to load available sites from database: {str(e)}")

def get_site_summary_data(site: str) -> Dict[str, any]:
    """
    Get site summary information for selected site.
    
    Args:
        site: Selected site name
    
    Returns:
        Dictionary with site summary data
    """
    
    db = get_database()
    
    try:
        query = """
        SELECT 
            SITE,
            SITE_GROUP,
            COUNT(DISTINCT BENEFICIARY_ID) as total_children,
            COUNT(DISTINCT HOUSEHOLD_ID) as total_households,
            COUNT(*) as total_measurements,
            ROUND(AVG(WHO_INDEX), 2) as avg_z_score,
            ROUND(SUM(CASE WHEN WHO_INDEX < -2 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 1) as stunting_rate
        FROM CHILD_NUTRITION_DATA 
        WHERE SITE = %(site)s
            AND FLAGGED = 0 AND DUPLICATE = 'False'
        GROUP BY SITE, SITE_GROUP
        """
        
        df = db.execute_query(query, {"site": site})
        
        if df.empty:
            raise Exception(f"No data found for site: {site}")
        else:
            # Safe data conversion with null handling
            row = df.iloc[0]
            
            # Clean and validate site group data
            site_group = str(row['SITE_GROUP']) if pd.notna(row['SITE_GROUP']) else ''
            
            # Filter out placeholder/invalid site groups
            invalid_groups = ['remove', 'delete', 'null', 'none', '', 'n/a', 'na']
            if site_group.lower().strip() in invalid_groups:
                # Use site name as fallback for site group
                site_name = str(row['SITE']) if pd.notna(row['SITE']) else 'Unknown Site'
                site_group = site_name  # Use site name as site group when invalid
            
            return {
                'site_name': str(row['SITE']) if pd.notna(row['SITE']) else 'Unknown Site',
                'site_group': site_group,
                'total_children': int(row['TOTAL_CHILDREN']) if pd.notna(row['TOTAL_CHILDREN']) else 0,
                'total_households': int(row['TOTAL_HOUSEHOLDS']) if pd.notna(row['TOTAL_HOUSEHOLDS']) else 0,
                'total_measurements': int(row['TOTAL_MEASUREMENTS']) if pd.notna(row['TOTAL_MEASUREMENTS']) else 0,
                'avg_z_score': float(row['AVG_Z_SCORE']) if pd.notna(row['AVG_Z_SCORE']) else 0.0,
                'stunting_rate': float(row['STUNTING_RATE']) if pd.notna(row['STUNTING_RATE']) else 0.0
            }
            
    except Exception as e:
        raise Exception(f"Failed to load site summary data for {site}: {str(e)}")

def get_site_rankings(site: str) -> Dict[str, Dict[str, any]]:
    """
    Get site rankings for performance cards.
    
    Args:
        site: Selected site name
    
    Returns:
        Dictionary with ranking data for each metric
    """
    
    db = get_database()
    
    try:
        # Children measured ranking
        children_query = """
        WITH site_rankings AS (
            SELECT 
                SITE,
                COUNT(DISTINCT BENEFICIARY_ID) as children_count,
                RANK() OVER (ORDER BY COUNT(DISTINCT BENEFICIARY_ID) DESC) as rank,
                COUNT(*) OVER () as total_sites
            FROM CHILD_NUTRITION_DATA 
            WHERE FLAGGED = 0 AND DUPLICATE = 'False'
            GROUP BY SITE
        )
        SELECT children_count, rank, total_sites
        FROM site_rankings 
        WHERE SITE = %(site)s
        """
        
        children_df = db.execute_query(children_query, {"site": site})
        
        # Average z-score ranking
        zscore_query = """
        WITH site_rankings AS (
            SELECT 
                SITE,
                AVG(WHO_INDEX) as avg_z_score,
                RANK() OVER (ORDER BY AVG(WHO_INDEX) DESC) as rank,
                COUNT(*) OVER () as total_sites
            FROM CHILD_NUTRITION_DATA 
            WHERE FLAGGED = 0 AND DUPLICATE = 'False'
            GROUP BY SITE
        )
        SELECT ROUND(avg_z_score, 2) as avg_z_score, rank, total_sites
        FROM site_rankings 
        WHERE SITE = %(site)s
        """
        
        zscore_df = db.execute_query(zscore_query, {"site": site})
        
        # Stunting rate ranking
        stunting_query = """
        WITH site_rankings AS (
            SELECT 
                SITE,
                SUM(CASE WHEN WHO_INDEX < -2 THEN 1 ELSE 0 END) * 100.0 / COUNT(*) as stunting_rate,
                RANK() OVER (ORDER BY SUM(CASE WHEN WHO_INDEX < -2 THEN 1 ELSE 0 END) * 100.0 / COUNT(*) ASC) as rank,
                COUNT(*) OVER () as total_sites
            FROM CHILD_NUTRITION_DATA 
            WHERE FLAGGED = 0 AND DUPLICATE = 'False'
            GROUP BY SITE
        )
        SELECT ROUND(stunting_rate, 1) as stunting_rate, rank, total_sites
        FROM site_rankings 
        WHERE SITE = %(site)s
        """
        
        stunting_df = db.execute_query(stunting_query, {"site": site})
        
        # Severe stunting ranking
        severe_stunting_query = """
        WITH site_rankings AS (
            SELECT 
                SITE,
                SUM(CASE WHEN WHO_INDEX < -3 THEN 1 ELSE 0 END) * 100.0 / COUNT(*) as severe_stunting_rate,
                RANK() OVER (ORDER BY SUM(CASE WHEN WHO_INDEX < -3 THEN 1 ELSE 0 END) * 100.0 / COUNT(*) ASC) as rank,
                COUNT(*) OVER () as total_sites
            FROM CHILD_NUTRITION_DATA 
            WHERE FLAGGED = 0 AND DUPLICATE = 'False'
            GROUP BY SITE
        )
        SELECT ROUND(severe_stunting_rate, 1) as severe_stunting_rate, rank, total_sites
        FROM site_rankings 
        WHERE SITE = %(site)s
        """
        
        severe_stunting_df = db.execute_query(severe_stunting_query, {"site": site})
        
        return {
            'children_measured': {
                'value': int(children_df.iloc[0]['CHILDREN_COUNT']) if not children_df.empty else 0,
                'rank': int(children_df.iloc[0]['RANK']) if not children_df.empty else 0,
                'total': int(children_df.iloc[0]['TOTAL_SITES']) if not children_df.empty else 0
            },
            'avg_z_score': {
                'value': float(zscore_df.iloc[0]['AVG_Z_SCORE']) if not zscore_df.empty else 0.0,
                'rank': int(zscore_df.iloc[0]['RANK']) if not zscore_df.empty else 0,
                'total': int(zscore_df.iloc[0]['TOTAL_SITES']) if not zscore_df.empty else 0
            },
            'stunting_rate': {
                'value': float(stunting_df.iloc[0]['STUNTING_RATE']) if not stunting_df.empty else 0.0,
                'rank': int(stunting_df.iloc[0]['RANK']) if not stunting_df.empty else 0,
                'total': int(stunting_df.iloc[0]['TOTAL_SITES']) if not stunting_df.empty else 0
            },
            'severe_stunting_rate': {
                'value': float(severe_stunting_df.iloc[0]['SEVERE_STUNTING_RATE']) if not severe_stunting_df.empty else 0.0,
                'rank': int(severe_stunting_df.iloc[0]['RANK']) if not severe_stunting_df.empty else 0,
                'total': int(severe_stunting_df.iloc[0]['TOTAL_SITES']) if not severe_stunting_df.empty else 0
            }
        }
        
    except Exception as e:
        raise Exception(f"Failed to load site rankings for {site}: {str(e)}")

def get_site_temporal_data(site: str) -> pd.DataFrame:
    """
    Get temporal trends data for selected site (Chart 1).
    
    Args:
        site: Selected site name
    
    Returns:
        DataFrame with temporal data
    """
    
    db = get_database()
    
    try:
        query = """
        SELECT 
            DATE_TRUNC('quarter', CAPTURE_DATE) as quarter,
            COUNT(*) as measurement_count,
            ROUND(AVG(WHO_INDEX), 2) as avg_z_score,
            ROUND(SUM(CASE WHEN WHO_INDEX BETWEEN -3 AND -2 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 1) as stunting_rate,
            ROUND(SUM(CASE WHEN WHO_INDEX < -3 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 1) as severe_stunting_rate
        FROM CHILD_NUTRITION_DATA 
        WHERE SITE = %(site)s
            AND FLAGGED = 0 AND DUPLICATE = 'False'
            AND CAPTURE_DATE >= DATEADD(year, -5, CURRENT_DATE())
        GROUP BY DATE_TRUNC('quarter', CAPTURE_DATE)
        ORDER BY quarter
        """
        
        df = db.execute_query(query, {"site": site})
        
        if df.empty:
            raise Exception(f"No temporal data found for site: {site}")
        else:
            # Process real data
            df['period'] = df['QUARTER'].astype(str)
            df['measurement_count'] = df['MEASUREMENT_COUNT'].astype(int)
            df['avg_z_score'] = df['AVG_Z_SCORE'].astype(float)
            df['stunting_rate'] = df['STUNTING_RATE'].astype(float)
            df['severe_stunting_rate'] = df['SEVERE_STUNTING_RATE'].astype(float)
            
            return df[['period', 'measurement_count', 'avg_z_score', 'stunting_rate', 'severe_stunting_rate']]
            
    except Exception as e:
        raise Exception(f"Failed to load temporal data for {site}: {str(e)}")

def get_site_category_data(site: str) -> pd.DataFrame:
    """
    Get category comparison data for selected site (Chart 2).
    
    Args:
        site: Selected site name
    
    Returns:
        DataFrame with category data
    """
    
    db = get_database()
    
    try:
        query = """
        WITH first_measurements AS (
            SELECT BENEFICIARY_ID, WHO_INDEX,
                   ROW_NUMBER() OVER (PARTITION BY BENEFICIARY_ID ORDER BY CAPTURE_DATE) as rn
            FROM CHILD_NUTRITION_DATA 
            WHERE SITE = %(site)s AND FLAGGED = 0 AND DUPLICATE = 'False'
        ),
        last_measurements AS (
            SELECT BENEFICIARY_ID, WHO_INDEX,
                   ROW_NUMBER() OVER (PARTITION BY BENEFICIARY_ID ORDER BY CAPTURE_DATE DESC) as rn
            FROM CHILD_NUTRITION_DATA 
            WHERE SITE = %(site)s AND FLAGGED = 0 AND DUPLICATE = 'False'
        ),
        site_totals AS (
            SELECT COUNT(DISTINCT BENEFICIARY_ID) as total
            FROM CHILD_NUTRITION_DATA 
            WHERE SITE = %(site)s AND FLAGGED = 0 AND DUPLICATE = 'False'
        )
        SELECT 
            'First Measurement' as period,
            SUM(CASE WHEN WHO_INDEX BETWEEN -2 AND -1 THEN 1 ELSE 0 END) as at_risk,
            SUM(CASE WHEN WHO_INDEX BETWEEN -3 AND -2 THEN 1 ELSE 0 END) as stunted,
            SUM(CASE WHEN WHO_INDEX < -3 THEN 1 ELSE 0 END) as severely_stunted
        FROM first_measurements WHERE rn = 1
        UNION ALL
        SELECT 
            'Last Measurement' as period,
            SUM(CASE WHEN WHO_INDEX BETWEEN -2 AND -1 THEN 1 ELSE 0 END) as at_risk,
            SUM(CASE WHEN WHO_INDEX BETWEEN -3 AND -2 THEN 1 ELSE 0 END) as stunted,
            SUM(CASE WHEN WHO_INDEX < -3 THEN 1 ELSE 0 END) as severely_stunted
        FROM last_measurements WHERE rn = 1
        UNION ALL
        SELECT 
            'Target' as period,
            CAST(total * 0.025 AS INTEGER) as at_risk,
            CAST(total * 0.025 AS INTEGER) as stunted,
            CAST(total * 0.0015 AS INTEGER) as severely_stunted
        FROM site_totals
        """
        
        df = db.execute_query(query, {"site": site})
        
        if df.empty:
            raise Exception(f"No category data found for site: {site}")
        else:
            # Process real data
            df['category'] = df['PERIOD']  # Rename 'period' to 'category' for chart compatibility
            df['at_risk'] = df['AT_RISK'].astype(int)
            df['stunted'] = df['STUNTED'].astype(int)
            df['severely_stunted'] = df['SEVERELY_STUNTED'].astype(int)
            
            return df[['category', 'at_risk', 'stunted', 'severely_stunted']]
            
    except Exception as e:
        raise Exception(f"Failed to load category data for {site}: {str(e)}")

def get_site_status_distribution(site: str) -> pd.DataFrame:
    """
    Get current status distribution for selected site (Chart 3).
    
    Args:
        site: Selected site name
    
    Returns:
        DataFrame with status distribution data
    """
    
    db = get_database()
    
    try:
        query = """
        WITH latest_measurements AS (
            SELECT BENEFICIARY_ID, WHO_INDEX,
                   ROW_NUMBER() OVER (PARTITION BY BENEFICIARY_ID ORDER BY CAPTURE_DATE DESC) as rn
            FROM CHILD_NUTRITION_DATA 
            WHERE SITE = %(site)s AND FLAGGED = 0 AND DUPLICATE = 'False'
        )
        SELECT 
            CASE 
                WHEN WHO_INDEX >= -1 THEN 'Normal'
                WHEN WHO_INDEX BETWEEN -2 AND -1 THEN 'At Risk'
                WHEN WHO_INDEX BETWEEN -3 AND -2 THEN 'Stunted'
                WHEN WHO_INDEX < -3 THEN 'Severely Stunted'
            END as status,
            COUNT(*) as count,
            ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 1) as percentage
        FROM latest_measurements
        WHERE rn = 1
        GROUP BY status
        ORDER BY 
            CASE status
                WHEN 'Normal' THEN 1
                WHEN 'At Risk' THEN 2
                WHEN 'Stunted' THEN 3
                WHEN 'Severely Stunted' THEN 4
            END
        """
        
        df = db.execute_query(query, {"site": site})
        
        if df.empty:
            raise Exception(f"No status distribution data found for site: {site}")
        else:
            # Process real data
            df['status'] = df['STATUS']
            df['count'] = df['COUNT'].astype(int)
            df['percentage'] = df['PERCENTAGE'].astype(float)
            
            return df[['status', 'count', 'percentage']]
            
    except Exception as e:
        raise Exception(f"Failed to load status distribution data for {site}: {str(e)}")

def get_z_score_comparison_data(selected_site: str) -> pd.DataFrame:
    """
    Get z-score comparison data across all sites (Chart 4).
    
    Args:
        selected_site: Currently selected site
    
    Returns:
        DataFrame with z-score comparison data
    """
    
    db = get_database()
    
    try:
        query = """
        SELECT 
            SITE,
            COUNT(DISTINCT BENEFICIARY_ID) as children_count,
            ROUND(AVG(WHO_INDEX), 2) as avg_z_score,
            CASE WHEN SITE = %(selected_site)s THEN 1 ELSE 0 END as is_current
        FROM CHILD_NUTRITION_DATA 
        WHERE FLAGGED = 0 AND DUPLICATE = 'False'
        GROUP BY SITE
        ORDER BY children_count DESC
        """
        
        df = db.execute_query(query, {"selected_site": selected_site})
        
        if df.empty:
            raise Exception("No z-score comparison data found")
        else:
            # Process real data
            df['site'] = df['SITE']
            df['children_count'] = df['CHILDREN_COUNT'].astype(int)
            df['avg_z_score'] = df['AVG_Z_SCORE'].astype(float)
            df['is_current'] = df['IS_CURRENT'].astype(bool)
            
            return df[['site', 'children_count', 'avg_z_score', 'is_current']]
            
    except Exception as e:
        raise Exception(f"Failed to load z-score comparison data: {str(e)}")

def get_stunting_comparison_data(selected_site: str) -> pd.DataFrame:
    """
    Get stunting rate comparison data across all sites (Chart 5).
    
    Args:
        selected_site: Currently selected site
    
    Returns:
        DataFrame with stunting comparison data
    """
    
    db = get_database()
    
    try:
        query = """
        SELECT 
            SITE,
            COUNT(DISTINCT BENEFICIARY_ID) as children_count,
            ROUND(SUM(CASE WHEN WHO_INDEX < -2 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 1) as stunting_rate,
            CASE WHEN SITE = %(selected_site)s THEN 1 ELSE 0 END as is_current
        FROM CHILD_NUTRITION_DATA 
        WHERE FLAGGED = 0 AND DUPLICATE = 'False'
        GROUP BY SITE
        ORDER BY stunting_rate ASC
        """
        
        df = db.execute_query(query, {"selected_site": selected_site})
        
        if df.empty:
            raise Exception("No stunting comparison data found")
        else:
            # Process real data
            df['site'] = df['SITE']
            df['children_count'] = df['CHILDREN_COUNT'].astype(int)
            df['stunting_rate'] = df['STUNTING_RATE'].astype(float)
            df['is_current'] = df['IS_CURRENT'].astype(bool)
            
            return df[['site', 'children_count', 'stunting_rate', 'is_current']]
            
    except Exception as e:
        raise Exception(f"Failed to load stunting comparison data: {str(e)}")

def get_measurement_volume_data(site: str) -> pd.DataFrame:
    """
    Get measurement volume over time for selected site (Chart 6).
    
    Args:
        site: Selected site name
    
    Returns:
        DataFrame with measurement volume data
    """
    
    db = get_database()
    
    try:
        query = """
        SELECT 
            DATE_TRUNC('quarter', CAPTURE_DATE) as quarter,
            COUNT(*) as measurement_count
        FROM CHILD_NUTRITION_DATA 
        WHERE SITE = %(site)s
            AND FLAGGED = 0 AND DUPLICATE = 'False'
            AND CAPTURE_DATE >= DATEADD(year, -5, CURRENT_DATE())
        GROUP BY DATE_TRUNC('quarter', CAPTURE_DATE)
        ORDER BY quarter
        """
        
        df = db.execute_query(query, {"site": site})
        
        if df.empty:
            raise Exception(f"No measurement volume data found for site: {site}")
        else:
            # Process real data
            df['period'] = df['QUARTER'].astype(str)
            df['measurement_count'] = df['MEASUREMENT_COUNT'].astype(int)
            
            return df[['period', 'measurement_count']]
            
    except Exception as e:
        raise Exception(f"Failed to load measurement volume data for {site}: {str(e)}")
