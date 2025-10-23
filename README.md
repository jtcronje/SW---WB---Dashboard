# Child Nutrition ETL Pipeline

A robust ETL pipeline for processing child nutrition measurement data and loading it into Snowflake.

## 🎯 **Overview**

This pipeline processes raw child nutrition data from Excel files, applies comprehensive data cleaning, and loads the cleaned data into Snowflake for analysis.

## 📁 **Project Structure**

```
├── src/                                    # Core source code
│   ├── __init__.py
│   ├── data_cleaning.py                   # Data cleaning functions
│   ├── data_validation.py                 # Data validation utilities
│   ├── derived_fields.py                  # Derived field calculations
│   ├── snowflake_integration.py           # Snowflake connection & upload
│   └── snowflake_loader.py                # Alternative Snowflake loader
├── main.py                                # Main pipeline entry point
├── requirements.txt                       # Python dependencies
├── env_template.txt                       # Environment variables template
├── data/
│   ├── raw/
│   │   └── raw_data_aug25.xlsx           # Original raw data
│   └── processed/
│       └── cleaned_nutrition_data_FIXED.csv  # Final cleaned data
└── README.md                              # This file
```

## 🚀 **Quick Start**

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set Environment Variables
Copy `env_template.txt` to `.env` and configure your Snowflake credentials:
```bash
cp env_template.txt .env
# Edit .env with your Snowflake credentials
```

### 3. Run the Pipeline
```bash
python main.py
```

## 🔧 **Data Cleaning Features**

- **Duplicate Removal**: Removes duplicate records based on key fields including Site
- **Extreme Value Removal**: Removes physiologically impossible measurements
- **Missing Data Handling**: Removes records with missing critical fields
- **Data Type Conversion**: Converts Excel serial dates and numeric fields
- **String Cleaning**: Enhanced cleaning with meaningful character replacement

## 📊 **Data Processing**

- **Input**: Excel file with child nutrition measurements
- **Output**: Cleaned CSV file ready for Snowflake upload
- **Records Processed**: ~36,050 clean records from 51,697 raw records
- **Data Quality**: 100% valid dates, no missing critical data

## 🏗️ **Snowflake Integration**

- **Database**: CHILD_NUTRITION_DB
- **Schema**: NUTRITION_DATA
- **Table**: CHILD_NUTRITION_DATA
- **Upload Method**: Chunked upload with error handling
- **Performance**: Optimized for large datasets

## 📈 **Pipeline Performance**

- **Duplicate Removal**: 30.2% reduction (15,607 duplicates removed)
- **Extreme Value Removal**: 0.1% reduction (38 extreme values removed)
- **Missing Data Removal**: 0.0% reduction (2 records with missing critical data)
- **Final Data Quality**: 100% clean records

## 🛠️ **Configuration**

The pipeline uses environment variables for configuration. See `env_template.txt` for required variables:

- `SNOWFLAKE_ACCOUNT`: Your Snowflake account identifier
- `SNOWFLAKE_USER`: Snowflake username
- `SNOWFLAKE_PASSWORD`: Snowflake password
- `SNOWFLAKE_DATABASE`: Target database name
- `SNOWFLAKE_SCHEMA`: Target schema name

## 📝 **Usage**

### Basic Usage
```python
from src.data_cleaning import *
from src.snowflake_integration import SnowflakeIntegration

# Load and clean data
df_cleaned = process_data('data/raw/raw_data_aug25.xlsx')

# Upload to Snowflake
sf = SnowflakeIntegration()
success = sf.upload_data(df_cleaned, 'CHILD_NUTRITION_DATA')
```

### Advanced Usage
```python
# Step-by-step processing
df = load_raw_data('data/raw/raw_data_aug25.xlsx')
df = remove_duplicates(df)
df = remove_extreme_values(df)
df = fix_data_types(df)
df = remove_missing_critical_data(df)
```

## 🔍 **Data Quality**

The pipeline ensures high data quality through:
- Comprehensive validation at each step
- Detailed logging of data transformations
- Error handling and recovery mechanisms
- Data quality metrics and reporting

## 📋 **Requirements**

- Python 3.9+
- pandas
- numpy
- snowflake-connector-python
- openpyxl
- python-dotenv

## 🎯 **Status**

✅ **Pipeline Status**: Fully functional
✅ **Data Quality**: 100% clean records
✅ **Snowflake Integration**: Working
✅ **Performance**: Optimized for production use

---

**Last Updated**: October 2024
**Version**: 1.0.0