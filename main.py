#!/usr/bin/env python3
"""
Child Nutrition Data ETL Pipeline - Main Entry Point

This script orchestrates the complete ETL pipeline for cleaning and ingesting
child nutrition measurement data from Excel files into Snowflake.

Usage:
    python main.py
    python main.py --no-upload
    python main.py --help
"""

import sys
import argparse
import logging
import pandas as pd
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def main():
    """Main entry point for the ETL pipeline."""
    parser = argparse.ArgumentParser(
        description='Child Nutrition Data ETL Pipeline'
    )
    parser.add_argument(
        '--no-upload',
        action='store_true',
        help='Skip Snowflake upload (clean data only)'
    )
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose logging'
    )
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Default paths
    input_path = 'data/raw/raw_data_aug25.xlsx'
    output_path = 'data/processed/cleaned_nutrition_data_FIXED.csv'
    
    # Validate input file exists
    if not Path(input_path).exists():
        logger.error(f"Input file not found: {input_path}")
        return 1
    
    try:
        logger.info("🚀 Starting Child Nutrition Data ETL Pipeline")
        logger.info(f"📁 Input file: {input_path}")
        logger.info(f"📁 Output file: {output_path}")
        logger.info(f"☁️ Upload to Snowflake: {not args.no_upload}")
        
        # Import pipeline modules
        from src.data_cleaning import (
            remove_duplicates, 
            remove_extreme_values, 
            remove_missing_critical_data, 
            fix_data_types
        )
        
        # Import Snowflake integration only if needed
        SnowflakeIntegration = None
        if not args.no_upload:
            try:
                from src.snowflake_integration import SnowflakeIntegration
            except ImportError as e:
                logger.error(f"❌ Snowflake integration not available: {e}")
                logger.info("⏭️ Continuing with data cleaning only...")
                args.no_upload = True
        
        # Step 1: Load raw data
        logger.info("📊 Loading raw data...")
        df_raw = pd.read_excel(input_path)
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
        df_cleaned.to_csv(output_path, index=False)
        logger.info(f"✅ Saved to: {output_path}")
        
        # Step 7: Upload to Snowflake (if not skipped)
        if not args.no_upload:
            logger.info("☁️ Uploading to Snowflake...")
            sf = SnowflakeIntegration()
            success = sf.upload_data(df_cleaned, 'CHILD_NUTRITION_DATA')
            
            if success:
                logger.info("✅ Snowflake upload completed successfully!")
            else:
                logger.error("❌ Snowflake upload failed!")
                return 1
        else:
            logger.info("⏭️ Skipping Snowflake upload")
        
        logger.info("🎉 ETL Pipeline completed successfully!")
        return 0
        
    except Exception as e:
        logger.error(f"❌ ETL Pipeline failed: {str(e)}")
        return 1

if __name__ == "__main__":
    sys.exit(main())



