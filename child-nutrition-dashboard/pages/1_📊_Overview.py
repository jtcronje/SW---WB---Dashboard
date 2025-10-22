"""
Overview Page - Child Nutrition Dashboard
Comprehensive nutrition analysis and monitoring dashboard.
Epic 1 Implementation: Complete overview with real data visualization.
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
import sys
import os

# Add utils directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from utils.components import (
    create_metric_card, create_stunting_progress_chart, create_temporal_trends_chart,
    create_sites_chart, create_program_distribution_chart, create_z_score_distribution_chart,
    add_ai_interpretation_button, add_export_button, create_loading_spinner,
    format_number_with_commas, COLORS
)
from utils.data_queries import (
    get_key_metrics, get_stunting_category_data, get_temporal_trends_data,
    get_top_sites_data, get_program_distribution_data, get_z_score_distribution_data
)

# Page configuration
st.set_page_config(
    page_title="Overview - Child Nutrition Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 32px;
        font-weight: bold;
        color: #2D3748;
        margin-bottom: 8px;
    }
    .main-subtitle {
        font-size: 16px;
        color: #718096;
        margin-bottom: 32px;
    }
    .chart-container {
        background: white;
        border-radius: 12px;
        padding: 24px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        border: 1px solid #E2E8F0;
        margin-bottom: 24px;
    }
    .metric-card {
        background: white;
        border-radius: 12px;
        padding: 24px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        border: 1px solid #E2E8F0;
        margin-bottom: 16px;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data(ttl=300)  # Cache for 5 minutes
def load_overview_data():
    """Load all data for the overview page with caching."""
    # Load all data
    metrics = get_key_metrics()
    percentage_data, count_data = get_stunting_category_data()
    temporal_data = get_temporal_trends_data()
    sites_data = get_top_sites_data()
    distribution_data = get_program_distribution_data()
    zscore_data = get_z_score_distribution_data()
    
    return {
        'metrics': metrics,
        'percentage_data': percentage_data,
        'count_data': count_data,
        'temporal_data': temporal_data,
        'sites_data': sites_data,
        'distribution_data': distribution_data,
        'zscore_data': zscore_data
    }

def main():
    """Main overview page content."""
    
    # Page header
    st.markdown('<div class="main-header">📊 Program Overview</div>', unsafe_allow_html=True)
    st.markdown('<div class="main-subtitle">Comprehensive child nutrition impact analysis • Last updated: ' + 
                datetime.now().strftime('%B %Y') + '</div>', unsafe_allow_html=True)
    
    # Load data with loading indicator
    try:
        with st.spinner("Loading dashboard data..."):
            data = load_overview_data()
    except Exception as e:
        st.error(f"Failed to load dashboard data: {str(e)}")
        st.info("Please check your database connection and ensure the NUTRITION_DATA table exists with the correct schema.")
        return
    
    # Key Metrics Section
    st.markdown("### 📈 Key Program Metrics")
    
    # Create columns for metrics
    col1, col2, col3, col4 = st.columns(4)
    
    metrics = data['metrics']
    
    with col1:
        create_metric_card(
            title="Total Children Measured",
            value=format_number_with_commas(metrics['total_children']),
            subtitle=f"Across {format_number_with_commas(metrics['total_children'])} unique children",
            icon="👶",
            color=COLORS['primary']
        )
    
    with col2:
        create_metric_card(
            title="Active Sites",
            value=str(metrics['active_sites']),
            subtitle="Across South Africa",
            icon="📍",
            color=COLORS['secondary']
        )
    
    with col3:
        create_metric_card(
            title="Stunting Reduction",
            value=f"{metrics['stunting_reduction']:.1f}%",
            subtitle="First to last measurement",
            icon="📈",
            trend=-metrics['stunting_reduction'],  # Negative because reduction is good
            color="#48BB78"
        )
    
    with col4:
        create_metric_card(
            title="Avg WHO Z-Score",
            value=f"{metrics['avg_zscore']:.2f}",
            subtitle="Improving toward 0 target",
            icon="📊",
            color=COLORS['atRisk']
        )
    
    st.markdown("---")
    
    # Chart 1: Stunting Category Progress (Percentage)
    st.markdown("### 📊 Stunting Category Progress (Percentage of Children)")
    
    with st.container():
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        
        fig1 = create_stunting_progress_chart(data['percentage_data'], "percentage")
        st.plotly_chart(fig1, use_container_width=True)
        
        # AI Interpretation and Export buttons
        col1, col2, col3 = st.columns([1, 1, 1])
        with col1:
            add_ai_interpretation_button("stunting-overview", "Stunting Category Progress")
        with col2:
            add_export_button(fig1, "stunting-progress")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Chart 2: Number of Children by Category
    st.markdown("### 👶 Number of Children by Stunting Category")
    
    with st.container():
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        
        fig2 = create_stunting_progress_chart(data['count_data'], "count")
        st.plotly_chart(fig2, use_container_width=True)
        
        # AI Interpretation and Export buttons
        col1, col2, col3 = st.columns([1, 1, 1])
        with col1:
            add_ai_interpretation_button("children-measured", "Children Measured by Category")
        with col2:
            add_export_button(fig2, "children-category")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Chart 3: Temporal Trends
    st.markdown("### 📈 Temporal Trends: Measurements & Stunting Rates")
    
    with st.container():
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        
        fig3 = create_temporal_trends_chart(data['temporal_data'])
        st.plotly_chart(fig3, use_container_width=True)
        
        # AI Interpretation and Export buttons
        col1, col2, col3 = st.columns([1, 1, 1])
        with col1:
            add_ai_interpretation_button("temporal-trends", "Temporal Trends")
        with col2:
            add_export_button(fig3, "temporal-trends")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Charts 4 & 5: Side by side
    st.markdown("### 🌍 Geographic Distribution & Program Performance")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Top Sites by Children Measured")
        with st.container():
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            
            fig4 = create_sites_chart(data['sites_data'])
            st.plotly_chart(fig4, use_container_width=True)
            
            # AI Interpretation and Export buttons
            col_a, col_b = st.columns(2)
            with col_a:
                add_ai_interpretation_button("geographic-reach", "Geographic Reach")
            with col_b:
                add_export_button(fig4, "top-sites")
            
            st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown("#### Program Distribution by Site Group")
        with st.container():
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            
            fig5 = create_program_distribution_chart(data['distribution_data'])
            st.plotly_chart(fig5, use_container_width=True)
            
            # AI Interpretation and Export buttons
            col_a, col_b = st.columns(2)
            with col_a:
                add_ai_interpretation_button("program-quality", "Program Distribution")
            with col_b:
                add_export_button(fig5, "program-distribution")
            
            st.markdown('</div>', unsafe_allow_html=True)
    
    # Chart 6: WHO Z-Score Distribution
    st.markdown("### 📊 WHO Height-for-Age Z-Score Analysis")
    
    with st.container():
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        
        # Add info box about current mean z-score
        current_mean = metrics['avg_zscore']
        st.info(f"""
        **Current Mean Z-Score: {current_mean:.2f}** • WHO Normal Range: -2 to +2 • Target: 0 (WHO median)
        """)
        
        fig6 = create_z_score_distribution_chart(data['zscore_data'])
        st.plotly_chart(fig6, use_container_width=True)
        
        # AI Interpretation and Export buttons
        col1, col2, col3 = st.columns([1, 1, 1])
        with col1:
            add_ai_interpretation_button("who-zscore", "WHO Z-Score Distribution")
        with col2:
            add_export_button(fig6, "zscore-distribution")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Footer
    st.markdown("---")
    st.markdown("**Epic 1 Implementation Complete** ✅ - All charts and metrics are now functional with real data integration.")
    
    # Data refresh button
    if st.button("🔄 Refresh Data"):
        st.cache_data.clear()
        st.experimental_rerun()

if __name__ == "__main__":
    main()
