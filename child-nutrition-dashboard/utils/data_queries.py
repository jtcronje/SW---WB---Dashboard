"""
Data Queries Module for Child Nutrition Dashboard
Contains all SQL queries and data processing functions for the Overview, Location, and Child pages.
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

# ============================================================================
# CHILD ANALYSIS PAGE QUERIES
# ============================================================================

def get_available_children_for_site(site: str, search_term: str = "") -> List[Dict]:
    """
    Get available children for a selected site with optional search filtering.
    
    Args:
        site: Selected site name
        search_term: Optional search term for filtering by name or ID
    
    Returns:
        List of dictionaries with child information
    """
    db = get_database()
    
    try:
        if not db.test_connection():
            raise Exception("Database connection test failed")
        
        # Build search condition
        search_condition = ""
        if search_term.strip():
            search_condition = f"""
                AND (
                    LOWER(FIRST_NAMES) LIKE LOWER('%{search_term}%')
                    OR LOWER(LAST_NAME) LIKE LOWER('%{search_term}%')
                    OR CAST(BENEFICIARY_ID AS VARCHAR) LIKE '%{search_term}%'
                )
            """
        
        query = f"""
        WITH child_summary AS (
            SELECT 
                BENEFICIARY_ID,
                FIRST_NAMES,
                LAST_NAME,
                HOUSEHOLD,
                SITE,
                COUNT(*) as measurement_count,
                MIN(CAPTURE_DATE) as first_measurement_date,
                MAX(CAPTURE_DATE) as last_measurement_date,
                ROUND(AVG(WHO_INDEX), 2) as avg_z_score
            FROM CHILD_NUTRITION_DATA 
            WHERE SITE = '{site}'
                AND FLAGGED = 0 AND DUPLICATE = 'False'
                {search_condition}
            GROUP BY BENEFICIARY_ID, FIRST_NAMES, LAST_NAME, HOUSEHOLD, SITE
        ),
        latest_measurements AS (
            SELECT 
                BENEFICIARY_ID,
                WHO_INDEX as latest_z_score,
                ROW_NUMBER() OVER (PARTITION BY BENEFICIARY_ID ORDER BY CAPTURE_DATE DESC) as rn
            FROM CHILD_NUTRITION_DATA 
            WHERE SITE = '{site}'
                AND FLAGGED = 0 AND DUPLICATE = 'False'
                {search_condition}
        )
        SELECT 
            cs.BENEFICIARY_ID,
            cs.FIRST_NAMES,
            cs.LAST_NAME,
            cs.HOUSEHOLD,
            cs.SITE,
            cs.measurement_count,
            cs.first_measurement_date,
            cs.last_measurement_date,
            cs.avg_z_score,
            lm.latest_z_score
        FROM child_summary cs
        LEFT JOIN latest_measurements lm ON cs.BENEFICIARY_ID = lm.BENEFICIARY_ID AND lm.rn = 1
        ORDER BY cs.FIRST_NAMES, cs.LAST_NAME
        LIMIT 50
        """
        
        df = db.execute_query(query)
        
        children = []
        for _, row in df.iterrows():
            # Format child name
            first_name = row['FIRST_NAMES'] if pd.notna(row['FIRST_NAMES']) else ""
            last_name = row['LAST_NAME'] if pd.notna(row['LAST_NAME']) else ""
            full_name = f"{first_name} {last_name}".strip()
            
            children.append({
                'beneficiary_id': row['BENEFICIARY_ID'],
                'name': full_name,
                'first_name': first_name,
                'last_name': last_name,
                'household': row['HOUSEHOLD'],
                'site': row['SITE'],
                'measurement_count': row['MEASUREMENT_COUNT'],
                'first_measurement_date': row['FIRST_MEASUREMENT_DATE'],
                'last_measurement_date': row['LAST_MEASUREMENT_DATE'],
                'avg_z_score': row['AVG_Z_SCORE'],
                'latest_z_score': row['LATEST_Z_SCORE']
            })
        
        return children
        
    except Exception as e:
        print(f"Error in get_available_children_for_site: {e}")
        return []

def get_child_profile_data(beneficiary_id: int) -> Dict:
    """
    Get comprehensive profile data for a specific child.
    
    Args:
        beneficiary_id: Child's beneficiary ID
    
    Returns:
        Dictionary with child profile information
    """
    db = get_database()
    
    try:
        if not db.test_connection():
            raise Exception("Database connection test failed")
        
        query = f"""
        WITH child_summary AS (
            SELECT 
                BENEFICIARY_ID,
                FIRST_NAMES,
                LAST_NAME,
                HOUSEHOLD,
                SITE,
                COUNT(*) as total_measurements,
                MIN(CAPTURE_DATE) as first_measurement_date,
                MAX(CAPTURE_DATE) as last_measurement_date,
                ROUND(DATEDIFF(day, MIN(CAPTURE_DATE), MAX(CAPTURE_DATE)) / 365.25, 1) as age_years,
                ROUND(AVG(WHO_INDEX), 2) as avg_z_score,
                MAX(ANSWER) - MIN(ANSWER) as height_gain_cm
            FROM CHILD_NUTRITION_DATA 
            WHERE BENEFICIARY_ID = {beneficiary_id}
                AND FLAGGED = 0 AND DUPLICATE = 'False'
            GROUP BY BENEFICIARY_ID, FIRST_NAMES, LAST_NAME, HOUSEHOLD, SITE
        ),
        latest_measurement AS (
            SELECT 
                BENEFICIARY_ID,
                WHO_INDEX as latest_z_score,
                ANSWER as latest_height,
                ROW_NUMBER() OVER (ORDER BY CAPTURE_DATE DESC) as rn
            FROM CHILD_NUTRITION_DATA 
            WHERE BENEFICIARY_ID = {beneficiary_id}
                AND FLAGGED = 0 AND DUPLICATE = 'False'
        )
        SELECT 
            cs.BENEFICIARY_ID,
            cs.FIRST_NAMES,
            cs.LAST_NAME,
            cs.HOUSEHOLD,
            cs.SITE,
            cs.total_measurements,
            cs.first_measurement_date,
            cs.last_measurement_date,
            cs.age_years,
            cs.avg_z_score,
            cs.height_gain_cm,
            lm.latest_z_score,
            lm.latest_height
        FROM child_summary cs
        LEFT JOIN latest_measurement lm ON cs.BENEFICIARY_ID = lm.BENEFICIARY_ID AND lm.rn = 1
        """
        
        df = db.execute_query(query)
        
        if df.empty:
            return {}
        
        row = df.iloc[0]
        
        # Format child name
        first_name = row['FIRST_NAMES'] if pd.notna(row['FIRST_NAMES']) else ""
        last_name = row['LAST_NAME'] if pd.notna(row['LAST_NAME']) else ""
        full_name = f"{first_name} {last_name}".strip()
        
        return {
            'beneficiary_id': row['BENEFICIARY_ID'],
            'name': full_name,
            'first_name': first_name,
            'last_name': last_name,
            'household': row['HOUSEHOLD'],
            'site': row['SITE'],
            'total_measurements': row['TOTAL_MEASUREMENTS'],
            'first_measurement_date': row['FIRST_MEASUREMENT_DATE'],
            'last_measurement_date': row['LAST_MEASUREMENT_DATE'],
            'age_years': row['AGE_YEARS'],
            'avg_z_score': row['AVG_Z_SCORE'],
            'latest_z_score': row['LATEST_Z_SCORE'],
            'latest_height': row['LATEST_HEIGHT'],
            'height_gain_cm': row['HEIGHT_GAIN_CM']
        }
        
    except Exception as e:
        print(f"Error in get_child_profile_data: {e}")
        return {}

def get_child_progress_metrics(beneficiary_id: int) -> Dict:
    """
    Get progress metrics for a specific child.
    
    Args:
        beneficiary_id: Child's beneficiary ID
    
    Returns:
        Dictionary with progress metrics
    """
    db = get_database()
    
    try:
        if not db.test_connection():
            raise Exception("Database connection test failed")
        
        query = f"""
        WITH child_summary AS (
            SELECT 
                MAX(ANSWER) - MIN(ANSWER) as height_gain_cm,
                ROUND(AVG(WHO_INDEX), 2) as avg_z_score,
                ROUND(DATEDIFF(month, MIN(CAPTURE_DATE), MAX(CAPTURE_DATE)), 1) as monitoring_months
            FROM CHILD_NUTRITION_DATA 
            WHERE BENEFICIARY_ID = {beneficiary_id}
                AND FLAGGED = 0 AND DUPLICATE = 'False'
        ),
        first_last_measurements AS (
            SELECT 
                FIRST_VALUE(WHO_INDEX) OVER (ORDER BY CAPTURE_DATE) as first_z_score,
                FIRST_VALUE(WHO_INDEX) OVER (ORDER BY CAPTURE_DATE DESC) as last_z_score,
                FIRST_VALUE(ANSWER) OVER (ORDER BY CAPTURE_DATE) as first_height,
                FIRST_VALUE(ANSWER) OVER (ORDER BY CAPTURE_DATE DESC) as last_height,
                ROW_NUMBER() OVER (ORDER BY CAPTURE_DATE) as first_rn,
                ROW_NUMBER() OVER (ORDER BY CAPTURE_DATE DESC) as last_rn
            FROM CHILD_NUTRITION_DATA 
            WHERE BENEFICIARY_ID = {beneficiary_id}
                AND FLAGGED = 0 AND DUPLICATE = 'False'
        )
        SELECT 
            cs.height_gain_cm,
            cs.avg_z_score,
            cs.monitoring_months,
            flm.first_z_score,
            flm.last_z_score,
            flm.first_height,
            flm.last_height,
            flm.last_z_score - flm.first_z_score as z_score_improvement,
            CASE 
                WHEN flm.first_z_score >= -1 THEN 'Normal'
                WHEN flm.first_z_score BETWEEN -2 AND -1 THEN 'At Risk'
                WHEN flm.first_z_score BETWEEN -3 AND -2 THEN 'Stunted'
                ELSE 'Severely Stunted'
            END as first_status,
            CASE 
                WHEN flm.last_z_score >= -1 THEN 'Normal'
                WHEN flm.last_z_score BETWEEN -2 AND -1 THEN 'At Risk'
                WHEN flm.last_z_score BETWEEN -3 AND -2 THEN 'Stunted'
                ELSE 'Severely Stunted'
            END as last_status
        FROM child_summary cs
        CROSS JOIN (
            SELECT 
                MAX(CASE WHEN first_rn = 1 THEN first_z_score END) as first_z_score,
                MAX(CASE WHEN last_rn = 1 THEN last_z_score END) as last_z_score,
                MAX(CASE WHEN first_rn = 1 THEN first_height END) as first_height,
                MAX(CASE WHEN last_rn = 1 THEN last_height END) as last_height
            FROM first_last_measurements
        ) flm
        """
        
        df = db.execute_query(query)
        
        if df.empty:
            return {}
        
        row = df.iloc[0]
        
        # Determine alert type based on status changes
        first_status = row['FIRST_STATUS']
        last_status = row['LAST_STATUS']
        
        if first_status != 'Normal' and last_status == 'Normal':
            alert_type = 'SUCCESS'
        elif first_status == 'Stunted' and last_status == 'At Risk':
            alert_type = 'WARNING'
        elif last_status in ['Stunted', 'Severely Stunted']:
            alert_type = 'INFO'
        else:
            alert_type = 'NORMAL'
        
        return {
            'height_gain_cm': row['HEIGHT_GAIN_CM'],
            'z_score_improvement': row['Z_SCORE_IMPROVEMENT'],
            'avg_z_score': row['AVG_Z_SCORE'],
            'monitoring_months': row['MONITORING_MONTHS'],
            'first_z_score': row['FIRST_Z_SCORE'],
            'last_z_score': row['LAST_Z_SCORE'],
            'first_height': row['FIRST_HEIGHT'],
            'last_height': row['LAST_HEIGHT'],
            'first_status': first_status,
            'last_status': last_status,
            'alert_type': alert_type
        }
        
    except Exception as e:
        print(f"Error in get_child_progress_metrics: {e}")
        return {}

def get_child_growth_trajectory(beneficiary_id: int) -> List[Dict]:
    """
    Get height growth trajectory data for a specific child.
    
    Args:
        beneficiary_id: Child's beneficiary ID
    
    Returns:
        List of dictionaries with measurement data over time
    """
    db = get_database()
    
    try:
        if not db.test_connection():
            raise Exception("Database connection test failed")
        
        query = f"""
        SELECT 
            CAPTURE_DATE,
            ANSWER as height_cm,
            WHO_INDEX,
            ROUND(DATEDIFF(day, 
                (SELECT MIN(CAPTURE_DATE) FROM CHILD_NUTRITION_DATA WHERE BENEFICIARY_ID = {beneficiary_id}), 
                CAPTURE_DATE) / 365.25, 1) as age_years
        FROM CHILD_NUTRITION_DATA 
        WHERE BENEFICIARY_ID = {beneficiary_id}
            AND FLAGGED = 0 AND DUPLICATE = 'False'
        ORDER BY CAPTURE_DATE
        """
        
        df = db.execute_query(query)
        
        trajectory = []
        for _, row in df.iterrows():
            trajectory.append({
                'date': row['CAPTURE_DATE'],
                'height_cm': row['HEIGHT_CM'],
                'z_score': row['WHO_INDEX'],
                'age_years': row['AGE_YEARS']
            })
        
        return trajectory
        
    except Exception as e:
        print(f"Error in get_child_growth_trajectory: {e}")
        return []

def get_child_z_score_progression(beneficiary_id: int) -> List[Dict]:
    """
    Get z-score progression data for a specific child.
    
    Args:
        beneficiary_id: Child's beneficiary ID
    
    Returns:
        List of dictionaries with z-score data over time
    """
    db = get_database()
    
    try:
        if not db.test_connection():
            raise Exception("Database connection test failed")
        
        query = f"""
        SELECT 
            CAPTURE_DATE,
            WHO_INDEX,
            ROUND(DATEDIFF(day, 
                (SELECT MIN(CAPTURE_DATE) FROM CHILD_NUTRITION_DATA WHERE BENEFICIARY_ID = {beneficiary_id}), 
                CAPTURE_DATE) / 365.25, 1) as age_years
        FROM CHILD_NUTRITION_DATA 
        WHERE BENEFICIARY_ID = {beneficiary_id}
            AND FLAGGED = 0 AND DUPLICATE = 'False'
        ORDER BY CAPTURE_DATE
        """
        
        df = db.execute_query(query)
        
        progression = []
        for _, row in df.iterrows():
            progression.append({
                'date': row['CAPTURE_DATE'],
                'z_score': row['WHO_INDEX'],
                'age_years': row['AGE_YEARS']
            })
        
        return progression
        
    except Exception as e:
        print(f"Error in get_child_z_score_progression: {e}")
        return []

def get_child_measurement_history(beneficiary_id: int) -> List[Dict]:
    """
    Get detailed measurement history for a specific child.
    
    Args:
        beneficiary_id: Child's beneficiary ID
    
    Returns:
        List of dictionaries with measurement history
    """
    db = get_database()
    
    try:
        if not db.test_connection():
            raise Exception("Database connection test failed")
        
        query = f"""
        WITH measurements_with_change AS (
            SELECT 
                CAPTURE_DATE,
                ANSWER as height_cm,
                WHO_INDEX,
                ROUND(DATEDIFF(day, 
                    (SELECT MIN(CAPTURE_DATE) FROM CHILD_NUTRITION_DATA WHERE BENEFICIARY_ID = {beneficiary_id}), 
                    CAPTURE_DATE) / 365.25, 1) as age_years,
                LAG(ANSWER) OVER (ORDER BY CAPTURE_DATE) as prev_height,
                LAG(WHO_INDEX) OVER (ORDER BY CAPTURE_DATE) as prev_z_score,
                ROW_NUMBER() OVER (ORDER BY CAPTURE_DATE) as row_num
            FROM CHILD_NUTRITION_DATA 
            WHERE BENEFICIARY_ID = {beneficiary_id}
                AND FLAGGED = 0 AND DUPLICATE = 'False'
        )
        SELECT 
            TO_CHAR(CAPTURE_DATE, 'YYYY-MM-DD') as date,
            age_years,
            height_cm,
            ROUND(WHO_INDEX, 2) as z_score,
            CASE 
                WHEN WHO_INDEX >= -1 THEN 'Normal'
                WHEN WHO_INDEX BETWEEN -2 AND -1 THEN 'At Risk'
                WHEN WHO_INDEX BETWEEN -3 AND -2 THEN 'Stunted'
                WHEN WHO_INDEX < -3 THEN 'Severely Stunted'
            END as status,
            CASE 
                WHEN row_num = 1 THEN 'First measurement'
                ELSE CONCAT(
                    CASE WHEN height_cm >= prev_height THEN '+' ELSE '' END,
                    ROUND(height_cm - prev_height, 1), 
                    ' cm | ',
                    CASE WHEN WHO_INDEX >= prev_z_score THEN '+' ELSE '' END,
                    ROUND(WHO_INDEX - prev_z_score, 2),
                    ' z'
                )
            END as change
        FROM measurements_with_change
        ORDER BY CAPTURE_DATE
        """
        
        df = db.execute_query(query)
        
        history = []
        for _, row in df.iterrows():
            history.append({
                'date': row['DATE'],
                'age_years': row['AGE_YEARS'],
                'height_cm': row['HEIGHT_CM'],
                'z_score': row['Z_SCORE'],
                'status': row['STATUS'],
                'change': row['CHANGE']
            })
        
        return history
        
    except Exception as e:
        print(f"Error in get_child_measurement_history: {e}")
        return []
