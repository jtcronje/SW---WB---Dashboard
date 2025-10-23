"""
Child Analysis Page - Child Nutrition Dashboard
Individual child nutrition tracking and insights.
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
import time

# Import utility modules
from utils.data_queries import (
    get_available_sites, 
    get_available_children_for_site,
    get_child_profile_data,
    get_child_progress_metrics,
    get_child_growth_trajectory,
    get_child_z_score_progression,
    get_child_measurement_history
)
from utils.components import (
    create_child_profile_card,
    create_progress_metric_card,
    create_alert_banner,
    create_growth_trajectory_chart,
    create_z_score_progression_chart,
    create_measurement_history_table
)

# Page configuration
st.set_page_config(
    page_title="Child Analysis - Child Nutrition Dashboard",
    page_icon="👶",
    layout="wide"
)

def main():
    """Main child analysis page content."""
    
    # Page header
    st.title("👶 Child Analysis")
    st.markdown("### Individual child nutrition tracking and insights")
    st.markdown("---")
    
    # Initialize session state
    if 'selected_site' not in st.session_state:
        st.session_state.selected_site = None
    if 'selected_child' not in st.session_state:
        st.session_state.selected_child = None
    if 'search_term' not in st.session_state:
        st.session_state.search_term = ""
    
    # Story 3.1: Child Selection & Profile
    st.subheader("🔍 Child Selection & Profile")
    
    # Get available sites
    try:
        sites_data = get_available_sites()
        site_options = ["Select a site..."] + sites_data['site'].tolist()
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            selected_site = st.selectbox(
                "📍 Select Location",
                options=site_options,
                index=0 if st.session_state.selected_site is None else site_options.index(st.session_state.selected_site) if st.session_state.selected_site in site_options else 0,
                key="site_selector"
            )
            
            if selected_site != "Select a site...":
                st.session_state.selected_site = selected_site
        
        with col2:
            search_term = st.text_input(
                "🔍 Search by Name or ID",
                value=st.session_state.search_term,
                placeholder="Enter child name or ID...",
                key="search_input"
            )
            st.session_state.search_term = search_term
        
        # Get children for selected site
        if st.session_state.selected_site and st.session_state.selected_site != "Select a site...":
            with st.spinner("Loading children..."):
                children_data = get_available_children_for_site(
                    st.session_state.selected_site, 
                    st.session_state.search_term
                )
            
            if children_data:
                # Create child options
                child_options = ["Select a child..."] + [
                    f"{child['name']} (ID: {child['beneficiary_id']})" 
                    for child in children_data
                ]
                
                selected_child_option = st.selectbox(
                    "👶 Select Child",
                    options=child_options,
                    index=0 if st.session_state.selected_child is None else 0,  # Reset selection
                    key="child_selector"
                )
                
                if selected_child_option != "Select a child...":
                    # Extract beneficiary ID from selection
                    child_id = int(selected_child_option.split("ID: ")[1].split(")")[0])
                    st.session_state.selected_child = child_id
                    
                    # Load child profile data
                    with st.spinner("Loading child profile..."):
                        child_profile = get_child_profile_data(child_id)
                        progress_metrics = get_child_progress_metrics(child_id)
                    
                    if child_profile:
                        # Display child profile card
                        create_child_profile_card(child_profile)
                        
                        # Story 3.2: Progress Metrics & Charts
                        st.markdown("---")
                        st.subheader("📊 Progress Metrics & Charts")
                        
                        if progress_metrics:
                            # Display alert banners based on status changes
                            alert_type = progress_metrics.get('alert_type', 'NORMAL')
                            if alert_type == 'SUCCESS':
                                create_alert_banner(
                                    'SUCCESS',
                                    'Excellent Progress!',
                                    f"Child has improved from {progress_metrics.get('first_status', 'Unknown')} to {progress_metrics.get('last_status', 'Unknown')}"
                                )
                            elif alert_type == 'WARNING':
                                create_alert_banner(
                                    'WARNING',
                                    'Improving but Still at Risk',
                                    f"Child has improved from {progress_metrics.get('first_status', 'Unknown')} to {progress_metrics.get('last_status', 'Unknown')} but requires continued monitoring"
                                )
                            elif alert_type == 'INFO':
                                create_alert_banner(
                                    'INFO',
                                    'Requires Continued Monitoring',
                                    f"Child remains {progress_metrics.get('last_status', 'Unknown')} and needs ongoing support"
                                )
                        
                        # Progress metric cards
                        col1, col2, col3, col4 = st.columns(4)
                        
                        with col1:
                            create_progress_metric_card(
                                "Height Gain",
                                f"{progress_metrics.get('height_gain_cm', 0):.1f} cm",
                                "Total growth during monitoring",
                                "📏",
                                "#4299E1"
                            )
                        
                        with col2:
                            create_progress_metric_card(
                                "Z-Score Improvement",
                                f"{progress_metrics.get('z_score_improvement', 0):+.2f}",
                                "Change in WHO z-score",
                                "📈",
                                "#68D391" if progress_metrics.get('z_score_improvement', 0) > 0 else "#FC8181"
                            )
                        
                        with col3:
                            create_progress_metric_card(
                                "Average Z-Score",
                                f"{progress_metrics.get('avg_z_score', 0):.2f}",
                                "Overall nutrition status",
                                "📊",
                                "#9F7AEA"
                            )
                        
                        with col4:
                            create_progress_metric_card(
                                "Monitoring Period",
                                f"{progress_metrics.get('monitoring_months', 0):.1f} months",
                                "Time under observation",
                                "⏱️",
                                "#F6AD55"
                            )
                        
                        # Charts section
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.markdown("#### 📈 Height Growth Trajectory")
                            growth_data = get_child_growth_trajectory(child_id)
                            if growth_data:
                                growth_chart = create_growth_trajectory_chart(growth_data)
                                st.plotly_chart(growth_chart, use_container_width=True)
                                
                                # AI interpretation button placeholder
                                if st.button("🧠 AI Interpretation", key="ai_growth"):
                                    st.info("AI interpretation functionality will be available in Epic 4")
                            else:
                                st.warning("No growth trajectory data available")
                        
                        with col2:
                            st.markdown("#### 📊 Z-Score Progression")
                            zscore_data = get_child_z_score_progression(child_id)
                            if zscore_data:
                                zscore_chart = create_z_score_progression_chart(zscore_data)
                                st.plotly_chart(zscore_chart, use_container_width=True)
                                
                                # AI interpretation button placeholder
                                if st.button("🧠 AI Interpretation", key="ai_zscore"):
                                    st.info("AI interpretation functionality will be available in Epic 4")
                            else:
                                st.warning("No z-score progression data available")
                        
                        # Story 3.3: Measurement History & AI Summary
                        st.markdown("---")
                        st.subheader("📋 Measurement History & AI Summary")
                        
                        measurement_history = get_child_measurement_history(child_id)
                        if measurement_history:
                            create_measurement_history_table(measurement_history)
                            
                            # AI Summary button placeholder
                            col1, col2, col3 = st.columns([1, 1, 1])
                            with col2:
                                if st.button("🧠 Generate AI Progress Summary", type="primary", key="ai_summary"):
                                    st.info("AI progress summary functionality will be available in Epic 4")
                        else:
                            st.warning("No measurement history available")
                    
                    else:
                        st.error("Error loading child profile data")
                else:
                    st.info("Please select a child to view their profile and progress")
            else:
                st.warning(f"No children found for site '{st.session_state.selected_site}' with search term '{st.session_state.search_term}'")
        else:
            st.info("Please select a site to view available children")
    
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        st.info("Please check your database connection and try again")
    
    # Footer
    st.markdown("---")

if __name__ == "__main__":
    main()
