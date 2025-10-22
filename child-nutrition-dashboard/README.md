# Child Nutrition Dashboard

A comprehensive Streamlit dashboard for child nutrition analysis and monitoring.

## Overview

This dashboard provides insights into child nutrition data with three main sections:
- **📊 Overview**: Comprehensive nutrition analysis and monitoring
- **📍 Location Analysis**: Geographic nutrition patterns and site performance
- **👶 Child Analysis**: Individual child nutrition tracking and insights

## Project Structure

```
child-nutrition-dashboard/
├── app.py                          # Main application entry point
├── requirements.txt                # Python dependencies
├── README.md                      # This file
├── .streamlit/
│   ├── config.toml               # Streamlit configuration
│   └── secrets.toml.template      # Secrets template
├── pages/                         # Dashboard pages
│   ├── 1_📊_Overview.py
│   ├── 2_📍_Location_Analysis.py
│   └── 3_👶_Child_Analysis.py
├── utils/                         # Utility functions
│   ├── __init__.py
│   └── database.py               # Database connection module
├── config/                        # Configuration files
└── assets/                        # Static assets
```

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Secrets

Copy the secrets template and fill in your credentials:

```bash
cp .streamlit/secrets.toml.template .streamlit/secrets.toml
```

Edit `.streamlit/secrets.toml` with your actual credentials:

```toml
[snowflake]
account = "your_account_identifier"
user = "your_username"
password = "your_password"
warehouse = "your_warehouse"
database = "your_database"
schema = "your_schema"
role = "your_role"

[openai]
api_key = "your_openai_api_key"

[app]
title = "Child Nutrition Dashboard"
description = "Comprehensive nutrition analysis and monitoring dashboard"
```

### 3. Run the Application

```bash
streamlit run app.py
```

## Features

### Current Features (Epic 0)
- ✅ Project structure setup
- ✅ Database connection module
- ✅ Placeholder pages with navigation
- ✅ Basic UI components and layout

### Upcoming Features
- **Epic 1**: Overview page with real data and charts
- **Epic 2**: Location analysis with geographic visualization
- **Epic 3**: Child analysis with individual profiles
- **Epic 4**: AI integration for insights and recommendations

## Database Schema

The dashboard connects to a Snowflake database with the following key columns:
- `BENEFICIARY_ID`: Unique child identifier
- `ANSWER`: Nutrition measurement value
- `WHO_INDEX`: WHO nutrition index
- `CAPTURE_DATE`: Date of measurement
- `SITE`: Site identifier
- `SITE_GROUP`: Site group classification
- `FIRST_NAMES`: Child's first name
- `LAST_NAME`: Child's last name
- `HOUSEHOLD`: Household identifier
- `HOUSEHOLD_ID`: Unique household ID
- `FLAGGED`: Data quality flag
- `DUPLICATE`: Duplicate record flag

## Development

### Running in Development Mode

```bash
streamlit run app.py --server.headless false
```

### Testing Database Connection

The database connection can be tested using the utility functions in `utils/database.py`:

```python
from utils.database import test_connection

if test_connection():
    print("Database connection successful!")
else:
    print("Database connection failed!")
```

## Configuration

### Streamlit Configuration

The dashboard uses the configuration in `.streamlit/config.toml` for:
- Theme settings
- Server configuration
- Browser settings
- Logging levels

### Database Configuration

Database connection parameters are stored in `.streamlit/secrets.toml` for security.

## Troubleshooting

### Common Issues

1. **Database Connection Failed**
   - Verify your Snowflake credentials in `secrets.toml`
   - Check network connectivity
   - Ensure the database and schema exist

2. **Import Errors**
   - Make sure all dependencies are installed: `pip install -r requirements.txt`
   - Check Python path configuration

3. **Page Not Loading**
   - Verify the page files are in the `pages/` directory
   - Check for syntax errors in the page files

## Support

For technical support or questions about the dashboard, please refer to the project documentation or contact the development team.

## License

This project is proprietary software developed for child nutrition monitoring and analysis.
