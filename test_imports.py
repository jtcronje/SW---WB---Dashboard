#!/usr/bin/env python3
"""
Test script to isolate import issues.
"""

import sys
import pandas as pd

print("Testing imports...")

try:
    print("1. Testing pandas import...")
    import pandas as pd
    print("✅ Pandas imported successfully")
except Exception as e:
    print(f"❌ Pandas import failed: {e}")

try:
    print("2. Testing data_cleaning import...")
    from src.data_cleaning import remove_duplicates
    print("✅ data_cleaning imported successfully")
except Exception as e:
    print(f"❌ data_cleaning import failed: {e}")

try:
    print("3. Testing snowflake_integration import...")
    from src.snowflake_integration import SnowflakeIntegration
    print("✅ snowflake_integration imported successfully")
except Exception as e:
    print(f"❌ snowflake_integration import failed: {e}")

print("Import test completed.")
