"""
Child Nutrition Dashboard - Main Application
A comprehensive Streamlit dashboard for child nutrition analysis and monitoring.
"""

import streamlit as st
import sys
import os
from pathlib import Path

# Add the utils directory to the Python path
current_dir = Path(__file__).parent
utils_dir = current_dir / "utils"
sys.path.append(str(utils_dir))

# Configure page
st.set_page_config(
    page_title="Child Nutrition Dashboard",
    page_icon="👶",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    """Main application entry point."""
    
    # Sidebar navigation
    st.sidebar.title("👶 Child Nutrition Dashboard")
    st.sidebar.markdown("---")
    
    # Navigation menu
    st.sidebar.markdown("### 📊 Navigation")
    
    # Page selection
    page = st.sidebar.selectbox(
        "Select a page:",
        [
            "📊 Overview",
            "📍 Location Analysis", 
            "👶 Child Analysis"
        ]
    )
    
    # Display selected page
    if page == "📊 Overview":
        show_overview_page()
    elif page == "📍 Location Analysis":
        show_location_page()
    elif page == "👶 Child Analysis":
        show_child_page()
    
    # Footer
    st.sidebar.markdown("---")
    st.sidebar.markdown("**Child Nutrition Dashboard**")
    st.sidebar.markdown("Version 1.0.0")

def show_overview_page():
    """Display the overview page."""
    st.title("📊 Overview")
    st.markdown("### Comprehensive nutrition analysis and monitoring")
    
    # Placeholder content
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Children", "1,234", "12%")
    
    with col2:
        st.metric("Active Sites", "45", "3%")
    
    with col3:
        st.metric("Nutrition Score", "8.2", "0.5")
    
    with col4:
        st.metric("Risk Cases", "23", "-5%")
    
    st.markdown("---")
    
    # Placeholder charts
    st.subheader("📈 Key Metrics")
    st.info("📊 Overview charts and analytics will be implemented in Epic 1")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Nutrition Trends")
        st.info("📈 Trend charts will be displayed here")
    
    with col2:
        st.subheader("Site Performance")
        st.info("📊 Site comparison charts will be displayed here")

def show_location_page():
    """Display the location analysis page."""
    st.title("📍 Location Analysis")
    st.markdown("### Geographic nutrition patterns and site performance")
    
    # Placeholder content
    st.info("🗺️ Location analysis features will be implemented in Epic 2")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Geographic Distribution")
        st.info("🗺️ Interactive maps will be displayed here")
    
    with col2:
        st.subheader("Site Rankings")
        st.info("📊 Site performance rankings will be shown here")
    
    st.markdown("---")
    st.subheader("Site Details")
    st.info("📋 Detailed site information and metrics will be available here")

def show_child_page():
    """Display the child analysis page."""
    st.title("👶 Child Analysis")
    st.markdown("### Individual child nutrition tracking and insights")
    
    # Placeholder content
    st.info("👶 Child analysis features will be implemented in Epic 3")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Child Search")
        st.info("🔍 Search and filter children by various criteria")
    
    with col2:
        st.subheader("Individual Profiles")
        st.info("👤 Detailed child nutrition profiles and history")
    
    st.markdown("---")
    st.subheader("Nutrition Insights")
    st.info("🧠 AI-powered nutrition insights and recommendations will be available here")

if __name__ == "__main__":
    main()
