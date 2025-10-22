#!/usr/bin/env python3
"""
Simple pipeline runner that avoids the Snowflake import issue.
"""

import sys
import pandas as pd
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    """Run the ETL pipeline without Snowflake upload."""
    try:
        logger.info("🚀 Starting Child Nutrition Data ETL Pipeline")
        
        # Import pipeline modules
        from src.data_cleaning import (
            remove_duplicates, 
            remove_extreme_values, 
            remove_missing_critical_data, 
            fix_data_types
        )
        
        # Step 1: Load raw data
        logger.info("📊 Loading raw data...")
        df_raw = pd.read_excel('data/raw/raw_data_aug25.xlsx')
        logger.info(f"✅ Loaded {len(df_raw):,} records")
        
        # Step 2: Remove duplicates
        logger.info("🔄 Removing duplicates...")
        df_step1 = remove_duplicates(df_raw)
        logger.info(f"✅ After duplicate removal: {len(df_step1):,} records")
        
        # Step 3: Remove extreme values
        logger.info("🔍 Removing extreme values...")
        df_step2 = remove_extreme_values(df_step1)
        logger.info(f"✅ After extreme value removal: {len(df_step2):,} records")
        
        # Step 4: Fix data types
        logger.info("🔧 Fixing data types...")
        df_step3 = fix_data_types(df_step2)
        logger.info(f"✅ After data type conversion: {len(df_step3):,} records")
        
        # Step 5: Remove missing critical data
        logger.info("🧹 Removing missing critical data...")
        df_cleaned = remove_missing_critical_data(df_step3)
        logger.info(f"✅ Final cleaned data: {len(df_cleaned):,} records")
        
        # Step 6: Save cleaned data
        logger.info("💾 Saving cleaned data...")
        df_cleaned.to_csv('data/processed/cleaned_nutrition_data_FIXED.csv', index=False)
        logger.info("✅ Saved to: data/processed/cleaned_nutrition_data_FIXED.csv")
        
        logger.info("🎉 ETL Pipeline completed successfully!")
        logger.info("📊 Data cleaning summary:")
        logger.info(f"   Raw records: {len(df_raw):,}")
        logger.info(f"   Cleaned records: {len(df_cleaned):,}")
        logger.info(f"   Records removed: {len(df_raw) - len(df_cleaned):,} ({(len(df_raw) - len(df_cleaned))/len(df_raw)*100:.1f}%)")
        
        return 0
        
    except Exception as e:
        logger.error(f"❌ ETL Pipeline failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
