"""
Location Analysis Page - Child Nutrition Dashboard
Site-specific nutrition outcomes and performance analysis.
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
import sys
import os

# Add the parent directory to the path to import utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.data_queries import (
    get_available_sites,
    get_site_rankings,
    get_site_temporal_data,
    get_site_category_data,
    get_site_status_distribution,
    get_z_score_comparison_data,
    get_stunting_comparison_data,
    get_measurement_volume_data
)
from utils.components import (
    create_ranking_card,
    create_site_temporal_chart,
    create_site_status_distribution_chart,
    create_z_score_comparison_chart,
    create_stunting_comparison_chart,
    create_measurement_volume_chart,
    create_stunting_progress_chart,
    add_ai_interpretation_button,
    add_export_button,
    create_loading_spinner
)

# Page configuration
st.set_page_config(
    page_title="Location Analysis - Child Nutrition Dashboard",
    page_icon="📍",
    layout="wide"
)

def main():
    """Main location analysis page content."""
    
    # Page header
    st.title("📍 Location Analysis")
    st.markdown("### Deep dive into site-specific nutrition outcomes")
    st.markdown("---")
    
    # Initialize session state for selected location
    if 'selected_location' not in st.session_state:
        st.session_state.selected_location = None
    
    try:
        # Load available sites
        with st.spinner("Loading available sites..."):
            sites_df = get_available_sites()
        
        if sites_df.empty:
            st.error("No sites found in the database. Please check your data connection.")
            return
        
        # Location selector
        st.subheader("🏢 Select Location")
        
        # Create site options with child count
        site_options = [f"{site} - {child_count:,} children" for site, child_count in 
                       zip(sites_df['site'], sites_df['child_count'])]
        
        selected_option = st.selectbox(
            "Choose a site to analyze:",
            options=site_options,
            index=0 if not st.session_state.selected_location else 
                  next((i for i, option in enumerate(site_options) 
                       if st.session_state.selected_location in option), 0),
            key="location_selector"
        )
        
        # Extract site name from selected option
        selected_site = selected_option.split(" - ")[0]
        
        # Update session state if location changed
        if st.session_state.selected_location != selected_site:
            st.session_state.selected_location = selected_site
            st.rerun()
        
        st.markdown("---")
        
        # Load site data
        with st.spinner(f"Loading data for {selected_site}..."):
            try:
                # Get site rankings
                site_rankings = get_site_rankings(selected_site)
                
                # Site summary card removed as requested
                
                # Performance ranking cards
                st.subheader("📊 Performance Rankings")
                
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    children_data = site_rankings['children_measured']
                    create_ranking_card(
                        title="Children Measured",
                        value=f"{children_data['value']:,}",
                        rank=children_data['rank'],
                        total=children_data['total'],
                        icon="👥",
                        color="#4299E1"
                    )
                
                with col2:
                    zscore_data = site_rankings['avg_z_score']
                    create_ranking_card(
                        title="Average Z-Score",
                        value=f"{zscore_data['value']:.2f}",
                        rank=zscore_data['rank'],
                        total=zscore_data['total'],
                        icon="📈",
                        color="#9F7AEA"
                    )
                
                with col3:
                    stunting_data = site_rankings['stunting_rate']
                    create_ranking_card(
                        title="Stunting Rate",
                        value=f"{stunting_data['value']:.1f}%",
                        rank=stunting_data['rank'],
                        total=stunting_data['total'],
                        icon="⚠️",
                        color="#FC8181"
                    )
                
                with col4:
                    severe_stunting_data = site_rankings['severe_stunting_rate']
                    create_ranking_card(
                        title="Severe Stunting",
                        value=f"{severe_stunting_data['value']:.1f}%",
                        rank=severe_stunting_data['rank'],
                        total=severe_stunting_data['total'],
                        icon="🚨",
                        color="#E53E3E"
                    )
                
                st.markdown("---")
                
                # Site-specific charts
                st.subheader("📈 Site-Specific Analysis")
                
                # Chart 1: Nutrition Outcomes Over Time
                st.markdown("#### Chart 1: Nutrition Outcomes Over Time")
                
                temporal_data = get_site_temporal_data(selected_site)
                temporal_chart = create_site_temporal_chart(temporal_data)
                st.plotly_chart(temporal_chart, use_container_width=True)
                
                # AI interpretation button for Chart 1
                add_ai_interpretation_button("temporal_chart", "Nutrition Outcomes Over Time")
                add_export_button(temporal_chart, "nutrition_outcomes")
                
                st.markdown("---")
                
                # Chart 2: Number of Children by Category
                st.markdown("#### Chart 2: Number of Children by Category")
                
                category_data = get_site_category_data(selected_site)
                category_chart = create_stunting_progress_chart(category_data, "count")
                st.plotly_chart(category_chart, use_container_width=True)
                
                # AI interpretation button for Chart 2
                add_ai_interpretation_button("category_chart", "Children by Category")
                add_export_button(category_chart, "children_by_category")
                
                st.markdown("---")
                
                # Chart 3: Current Status Distribution
                st.markdown("#### Chart 3: Current Status Distribution")
                
                status_data = get_site_status_distribution(selected_site)
                status_chart = create_site_status_distribution_chart(status_data)
                st.plotly_chart(status_chart, use_container_width=True)
                
                # AI interpretation button for Chart 3
                add_ai_interpretation_button("status_chart", "Status Distribution")
                add_export_button(status_chart, "status_distribution")
                
                st.markdown("---")
                
                # Comparison charts
                st.subheader("🔍 Cross-Site Comparison")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    # Chart 4: Z-Score Comparison
                    st.markdown("#### Chart 4: Z-Score Comparison Across Locations")
                    
                    zscore_comparison_data = get_z_score_comparison_data(selected_site)
                    zscore_comparison_chart = create_z_score_comparison_chart(zscore_comparison_data, selected_site)
                    st.plotly_chart(zscore_comparison_chart, use_container_width=True)
                    
                    # AI interpretation button for Chart 4
                    add_ai_interpretation_button("zscore_comparison", "Z-Score Comparison")
                    add_export_button(zscore_comparison_chart, "zscore_comparison")
                
                with col2:
                    # Chart 5: Stunting Rate Comparison
                    st.markdown("#### Chart 5: Stunting Rate Comparison")
                    
                    stunting_comparison_data = get_stunting_comparison_data(selected_site)
                    stunting_comparison_chart = create_stunting_comparison_chart(stunting_comparison_data, selected_site)
                    st.plotly_chart(stunting_comparison_chart, use_container_width=True)
                    
                    # AI interpretation button for Chart 5
                    add_ai_interpretation_button("stunting_comparison", "Stunting Rate Comparison")
                    add_export_button(stunting_comparison_chart, "stunting_comparison")
                
                st.markdown("---")
                
                # Chart 6: Measurement Volume Over Time
                st.markdown("#### Chart 6: Measurement Volume Over Time")
                
                volume_data = get_measurement_volume_data(selected_site)
                volume_chart = create_measurement_volume_chart(volume_data)
                st.plotly_chart(volume_chart, use_container_width=True)
                
                # AI interpretation button for Chart 6
                add_ai_interpretation_button("volume_chart", "Measurement Volume")
                add_export_button(volume_chart, "measurement_volume")
                
            except Exception as e:
                st.error(f"Error loading data for {selected_site}: {str(e)}")
                st.info("Please try selecting a different site or contact support if the issue persists.")
                return
        
    except Exception as e:
        st.error(f"Error loading location analysis data: {str(e)}")
        st.info("Please check your database connection and try again.")
        return
    
    # Footer
    st.markdown("---")
    st.markdown(f"**Last Updated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | **Selected Site:** {st.session_state.selected_location}")

if __name__ == "__main__":
    main()
