"""
Data validation functions for child nutrition measurement data.

This module contains functions to validate data quality and create
comprehensive data quality reports.
"""

import pandas as pd
import numpy as np
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)


def validate_data_quality(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Validate data quality and return quality metrics.
    
    Parameters:
    df (DataFrame): Data to validate
    
    Returns:
    Dict: Data quality metrics
    """
    quality_metrics = {
        'total_records': len(df),
        'unique_children': df['BeneficiaryId'].nunique(),
        'missing_data': df.isnull().sum().to_dict(),
        'data_types': df.dtypes.to_dict(),
        'date_range': {
            'start': df['Capture Date'].min(),
            'end': df['Capture Date'].max()
        }
    }
    
    logger.info(f"Data quality validation completed for {len(df)} records")
    return quality_metrics


def create_quality_report(df: pd.DataFrame) -> str:
    """
    Create a comprehensive data quality report.
    
    Parameters:
    df (DataFrame): Data to analyze
    
    Returns:
    str: Quality report as formatted string
    """
    report = []
    report.append("=" * 70)
    report.append("CHILD NUTRITION DATA QUALITY REPORT")
    report.append("=" * 70)
    
    # Basic statistics
    report.append(f"\nTotal Records: {len(df):,}")
    report.append(f"Unique Children: {df['BeneficiaryId'].nunique():,}")
    report.append(f"Date Range: {df['Capture Date'].min()} to {df['Capture Date'].max()}")
    
    # Missing data analysis
    report.append("\nMissing Data Analysis:")
    missing_data = df.isnull().sum()
    for field, count in missing_data.items():
        if count > 0:
            percentage = (count / len(df)) * 100
            report.append(f"  {field}: {count:,} ({percentage:.1f}%)")
    
    # Data type analysis
    report.append("\nData Types:")
    for field, dtype in df.dtypes.items():
        report.append(f"  {field}: {dtype}")
    
    return "\n".join(report)



