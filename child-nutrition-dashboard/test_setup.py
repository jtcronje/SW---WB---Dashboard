#!/usr/bin/env python3
"""
Test script to verify the Child Nutrition Dashboard setup.
This script tests the basic functionality without requiring database credentials.
"""

import sys
import os
from pathlib import Path

def test_imports():
    """Test that all required modules can be imported."""
    print("🧪 Testing imports...")
    
    try:
        import streamlit as st
        print("✅ Streamlit imported successfully")
    except ImportError as e:
        print(f"❌ Streamlit import failed: {e}")
        return False
    
    try:
        import pandas as pd
        print("✅ Pandas imported successfully")
    except ImportError as e:
        print(f"❌ Pandas import failed: {e}")
        return False
    
    try:
        import plotly.express as px
        import plotly.graph_objects as go
        print("✅ Plotly imported successfully")
    except ImportError as e:
        print(f"❌ Plotly import failed: {e}")
        return False
    
    try:
        import snowflake.connector
        print("✅ Snowflake connector imported successfully")
    except ImportError as e:
        print(f"❌ Snowflake connector import failed: {e}")
        return False
    
    return True

def test_file_structure():
    """Test that all required files exist."""
    print("\n📁 Testing file structure...")
    
    required_files = [
        "app.py",
        "requirements.txt",
        "README.md",
        ".streamlit/config.toml",
        ".streamlit/secrets.toml.template",
        "pages/1_📊_Overview.py",
        "pages/2_📍_Location_Analysis.py", 
        "pages/3_👶_Child_Analysis.py",
        "utils/__init__.py",
        "utils/database.py"
    ]
    
    all_exist = True
    for file_path in required_files:
        if Path(file_path).exists():
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} - MISSING")
            all_exist = False
    
    return all_exist

def test_database_module():
    """Test that the database module can be imported."""
    print("\n🗄️ Testing database module...")
    
    try:
        # Add utils to path
        sys.path.append(str(Path("utils")))
        
        from utils.database import DatabaseConnection, get_database
        print("✅ Database module imported successfully")
        
        # Test that we can create a database instance (without connecting)
        db = DatabaseConnection()
        print("✅ Database connection class created successfully")
        
        return True
    except Exception as e:
        print(f"❌ Database module test failed: {e}")
        return False

def test_pages():
    """Test that all pages can be imported."""
    print("\n📄 Testing pages...")
    
    pages = [
        "pages.1_📊_Overview",
        "pages.2_📍_Location_Analysis", 
        "pages.3_👶_Child_Analysis"
    ]
    
    all_imported = True
    for page in pages:
        try:
            __import__(page)
            print(f"✅ {page}")
        except Exception as e:
            print(f"❌ {page} - {e}")
            all_imported = False
    
    return all_imported

def main():
    """Run all tests."""
    print("🚀 Child Nutrition Dashboard - Setup Test")
    print("=" * 50)
    
    tests = [
        ("Import Test", test_imports),
        ("File Structure Test", test_file_structure),
        ("Database Module Test", test_database_module),
        ("Pages Test", test_pages)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n🔍 Running {test_name}...")
        result = test_func()
        results.append((test_name, result))
    
    print("\n" + "=" * 50)
    print("📊 Test Results Summary:")
    
    all_passed = True
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{status} - {test_name}")
        if not result:
            all_passed = False
    
    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 All tests passed! The dashboard setup is ready.")
        print("\n📋 Next steps:")
        print("1. Copy .streamlit/secrets.toml.template to .streamlit/secrets.toml")
        print("2. Fill in your Snowflake credentials in secrets.toml")
        print("3. Run: streamlit run app.py")
    else:
        print("❌ Some tests failed. Please check the errors above.")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
