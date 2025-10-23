"""
Reusable Components for Child Nutrition Dashboard
Contains UI components, chart utilities, and helper functions.
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta

# Color palette matching the mockup
COLORS = {
    'atRisk': '#F6AD55',      # Orange
    'stunted': '#FC8181',     # Coral/Red
    'severelyStunted': '#E53E3E',  # Dark Red
    'normal': '#68D391',      # Green
    'primary': '#4299E1',     # Blue
    'secondary': '#9F7AEA',   # Purple
    'background': '#F7FAFC',  # Light Gray
    'text': '#2D3748',        # Dark Gray
    'textSecondary': '#718096' # Medium Gray
}

def create_metric_card(title: str, value: str, subtitle: str = None, 
                      icon: str = "📊", trend: Optional[float] = None, 
                      color: str = COLORS['primary']) -> None:
    """
    Create a styled metric card component using Streamlit's native metric.
    
    Args:
        title: Card title
        value: Main metric value
        subtitle: Optional subtitle text
        icon: Icon emoji
        trend: Optional trend percentage (positive = improvement)
        color: Card accent color
    """
    
    # Format the trend for Streamlit metric
    if trend is not None:
        trend_formatted = f"{abs(trend):.1f}%"
        delta_color = "normal" if trend > 0 else "inverse"
    else:
        trend_formatted = None
        delta_color = "normal"
    
    # Use Streamlit's native metric component
    st.metric(
        label=f"{icon} {title}",
        value=value,
        delta=trend_formatted,
        delta_color=delta_color,
        help=subtitle
    )

def create_stunting_progress_chart(data: pd.DataFrame, chart_type: str = "percentage") -> go.Figure:
    """
    Create stunting category progress chart (Chart 1 & 2).
    
    Args:
        data: DataFrame with stunting category data
        chart_type: "percentage" or "count"
    
    Returns:
        Plotly figure
    """
    
    # Prepare data for grouped bar chart
    categories = data['category'].tolist()
    at_risk = data['at_risk'].tolist()
    stunted = data['stunted'].tolist()
    severely_stunted = data['severely_stunted'].tolist()
    
    fig = go.Figure()
    
    # Add bars for each category
    fig.add_trace(go.Bar(
        name='At Risk of Stunting',
        x=categories,
        y=at_risk,
        marker_color=COLORS['atRisk'],
        marker=dict(line=dict(width=0))
    ))
    
    fig.add_trace(go.Bar(
        name='Stunted',
        x=categories,
        y=stunted,
        marker_color=COLORS['stunted'],
        marker=dict(line=dict(width=0))
    ))
    
    fig.add_trace(go.Bar(
        name='Severely Stunted',
        x=categories,
        y=severely_stunted,
        marker_color=COLORS['severelyStunted'],
        marker=dict(line=dict(width=0))
    ))
    
    # Update layout
    y_axis_title = 'Percentage (%)' if chart_type == "percentage" else 'Number of Children'
    chart_title = 'Stunting Category Progress (Percentage of Children)' if chart_type == "percentage" else 'Number of Children by Stunting Category'
    
    fig.update_layout(
        title=chart_title,
        xaxis_title='Measurement Period',
        yaxis_title=y_axis_title,
        barmode='group',
        height=400,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color=COLORS['text']),
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    # Update axes
    fig.update_xaxes(
        gridcolor='#E2E8F0',
        linecolor='#718096',
        tickcolor='#718096'
    )
    fig.update_yaxes(
        gridcolor='#E2E8F0',
        linecolor='#718096',
        tickcolor='#718096'
    )
    
    return fig

def create_temporal_trends_chart(data: pd.DataFrame) -> go.Figure:
    """
    Create temporal trends chart with dual y-axes (Chart 3).
    
    Args:
        data: DataFrame with temporal data
    
    Returns:
        Plotly figure with dual y-axes
    """
    
    fig = make_subplots(
        rows=1, cols=1,
        specs=[[{"secondary_y": True}]]
    )
    
    # Add area chart for measurements
    fig.add_trace(
        go.Scatter(
            x=data['period'],
            y=data['measurements'],
            mode='lines',
            fill='tonexty',
            fillcolor='rgba(66, 153, 225, 0.19)',  # #4299E1 with 30/255 alpha
            line=dict(color=COLORS['primary'], width=3),
            name='Measurements',
            yaxis='y'
        ),
        secondary_y=False,
    )
    
    # Add line chart for stunting rate
    fig.add_trace(
        go.Scatter(
            x=data['period'],
            y=data['stunting_rate'],
            mode='lines+markers',
            line=dict(color=COLORS['severelyStunted'], width=3),
            marker=dict(size=6),
            name='Stunting %',
            yaxis='y2'
        ),
        secondary_y=True,
    )
    
    # Update layout
    fig.update_layout(
        title='Temporal Trends: Measurements & Stunting Rates',
        height=400,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color=COLORS['text']),
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    # Update axes
    fig.update_xaxes(
        gridcolor='#E2E8F0',
        linecolor='#718096',
        tickcolor='#718096',
        tickangle=-45
    )
    
    # Set y-axes titles
    fig.update_yaxes(
        title_text="Measurements",
        secondary_y=False,
        gridcolor='#E2E8F0',
        linecolor='#718096',
        tickcolor='#718096'
    )
    fig.update_yaxes(
        title_text="Stunting %",
        secondary_y=True,
        gridcolor='#E2E8F0',
        linecolor='#718096',
        tickcolor='#718096'
    )
    
    return fig

def create_sites_chart(data: pd.DataFrame) -> go.Figure:
    """
    Create horizontal bar chart for top sites (Chart 4).
    
    Args:
        data: DataFrame with site data
    
    Returns:
        Plotly figure
    """
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=data['children_count'],
        y=data['site'],
        orientation='h',
        marker_color=COLORS['primary'],
        marker=dict(line=dict(width=0)),
        text=data['children_count'],
        textposition='auto',
    ))
    
    fig.update_layout(
        title='Top Sites by Children Measured',
        xaxis_title='Number of Children',
        yaxis_title='',
        height=400,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color=COLORS['text']),
        showlegend=False
    )
    
    fig.update_xaxes(
        gridcolor='#E2E8F0',
        linecolor='#718096',
        tickcolor='#718096'
    )
    fig.update_yaxes(
        gridcolor='#E2E8F0',
        linecolor='#718096',
        tickcolor='#718096'
    )
    
    return fig

def create_program_distribution_chart(data: pd.DataFrame) -> go.Figure:
    """
    Create pie chart for program distribution (Chart 5).
    
    Args:
        data: DataFrame with site group data
    
    Returns:
        Plotly figure
    """
    
    # Define colors for pie chart
    colors = [COLORS['primary'], COLORS['secondary'], COLORS['atRisk'], '#48BB78', '#9F7AEA']
    
    fig = go.Figure(data=[go.Pie(
        labels=data['site_group'],
        values=data['percentage'],
        textinfo='label+percent',
        textposition='auto',
        marker=dict(colors=colors[:len(data)]),
        hovertemplate='<b>%{label}</b><br>%{percent}<br>(%{value:.1f}%)<extra></extra>'
    )])
    
    fig.update_layout(
        title='Program Distribution by Site Group',
        height=400,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color=COLORS['text']),
        showlegend=True
    )
    
    return fig

def create_z_score_distribution_chart(data: pd.DataFrame) -> go.Figure:
    """
    Create line chart for WHO Z-Score distribution (Chart 6).
    
    Args:
        data: DataFrame with z-score distribution data
    
    Returns:
        Plotly figure
    """
    
    fig = go.Figure()
    
    # Add main distribution line
    fig.add_trace(go.Scatter(
        x=data['z_score_bin'],
        y=data['frequency'],
        mode='lines+markers',
        line=dict(color=COLORS['primary'], width=3),
        marker=dict(size=6),
        name='Z-Score Distribution'
    ))
    
    # Add reference lines for WHO standards
    fig.add_hline(y=0, line_dash="dash", line_color=COLORS['severelyStunted'], 
                  annotation_text="Severe Stunting Threshold (-3)", annotation_position="top right")
    fig.add_hline(y=0, line_dash="dash", line_color=COLORS['stunted'], 
                  annotation_text="Stunting Threshold (-2)", annotation_position="top right")
    fig.add_hline(y=0, line_dash="dash", line_color=COLORS['normal'], 
                  annotation_text="WHO Median (0)", annotation_position="top right")
    
    fig.update_layout(
        title='WHO Height-for-Age Z-Score Analysis',
        xaxis_title='Z-Score',
        yaxis_title='Number of Children',
        height=400,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color=COLORS['text']),
        showlegend=True
    )
    
    fig.update_xaxes(
        gridcolor='#E2E8F0',
        linecolor='#718096',
        tickcolor='#718096'
    )
    fig.update_yaxes(
        gridcolor='#E2E8F0',
        linecolor='#718096',
        tickcolor='#718096'
    )
    
    return fig

def add_ai_interpretation_button(chart_id: str, chart_title: str) -> None:
    """
    Add AI interpretation button placeholder.
    
    Args:
        chart_id: Unique identifier for the chart
        chart_title: Title of the chart for AI interpretation
    """
    
    if st.button(f"🤖 Get AI Interpretation - {chart_title}", key=f"ai_{chart_id}"):
        st.info(f"AI interpretation for {chart_title} will be available in Epic 4 (AI Integration). This feature will provide intelligent insights and recommendations based on the data visualization.")

def add_export_button(fig: go.Figure, filename: str) -> None:
    """
    Add chart export functionality.
    
    Args:
        fig: Plotly figure
        filename: Base filename for export
    """
    
    # Use a simple container layout instead of columns to avoid nesting issues
    container = st.container()
    
    with container:
        if st.button(f"📊 Export as PNG - {filename}", key=f"export_png_{filename}"):
            st.success(f"PNG export for {filename} would be implemented here.")
        
        if st.button(f"📄 Export as PDF - {filename}", key=f"export_pdf_{filename}"):
            st.success(f"PDF export for {filename} would be implemented here.")

def create_loading_spinner(message: str = "Loading data..."):
    """
    Create a loading spinner component.
    
    Args:
        message: Loading message to display
    """
    
    spinner_html = f"""
    <div style="
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 40px;
        background: white;
        border-radius: 12px;
        border: 1px solid #E2E8F0;
    ">
        <div style="
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 16px;
        ">
            <div style="
                width: 40px;
                height: 40px;
                border: 4px solid #E2E8F0;
                border-top: 4px solid {COLORS['primary']};
                border-radius: 50%;
                animation: spin 1s linear infinite;
            "></div>
            <div style="color: {COLORS['textSecondary']}; font-size: 14px;">
                {message}
            </div>
        </div>
    </div>
    
    <style>
    @keyframes spin {{
        0% {{ transform: rotate(0deg); }}
        100% {{ transform: rotate(360deg); }}
    }}
    </style>
    """
    
    st.markdown(spinner_html, unsafe_allow_html=True)

def format_number_with_commas(number) -> str:
    """
    Format number with commas for better readability.
    
    Args:
        number: Number to format (handles None/NaN values)
    
    Returns:
        Formatted string
    """
    if number is None or pd.isna(number):
        return "0"
    try:
        return f"{int(number):,}"
    except (ValueError, TypeError):
        return "0"

def format_percentage(number) -> str:
    """
    Format number as percentage with proper null handling.
    
    Args:
        number: Number to format as percentage (handles None/NaN values)
    
    Returns:
        Formatted percentage string
    """
    if number is None or pd.isna(number):
        return "0.0%"
    try:
        return f"{float(number):.1f}%"
    except (ValueError, TypeError):
        return "0.0%"

def calculate_percentage_change(old_value: float, new_value: float) -> float:
    """
    Calculate percentage change between two values.
    
    Args:
        old_value: Original value
        new_value: New value
    
    Returns:
        Percentage change
    """
    if old_value == 0:
        return 0
    return ((new_value - old_value) / old_value) * 100

# ============================================================================
# LOCATION ANALYSIS PAGE COMPONENTS
# ============================================================================

def create_site_summary_card(site_data: Dict[str, any]) -> None:
    """
    Create site summary hero card with gradient background.
    
    Args:
        site_data: Dictionary with site summary information
    """
    
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #667EEA 0%, #764BA2 100%);
        border-radius: 16px;
        padding: 32px;
        margin: 24px 0;
        color: white;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
    ">
        <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 24px;">
            <div>
                <h2 style="margin: 0; font-size: 32px; font-weight: 700; color: white;">
                    {site_data['site_name']}
                </h2>
                <p style="margin: 8px 0 0 0; font-size: 16px; color: rgba(255,255,255,0.9);">
                    📍 {site_data['site_group']}
                </p>
            </div>
            <div style="text-align: right;">
                <div style="font-size: 14px; color: rgba(255,255,255,0.8); margin-bottom: 4px;">
                    Avg Z-Score
                </div>
                <div style="font-size: 24px; font-weight: 700; color: white;">
                    {site_data['avg_z_score']:.2f}
                </div>
            </div>
        </div>
        
        <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 24px;">
            <div style="text-align: center;">
                <div style="font-size: 28px; font-weight: 700; color: white; margin-bottom: 4px;">
                    {format_number_with_commas(site_data['total_children'])}
                </div>
                <div style="font-size: 14px; color: rgba(255,255,255,0.8);">
                    Children
                </div>
            </div>
            <div style="text-align: center;">
                <div style="font-size: 28px; font-weight: 700; color: white; margin-bottom: 4px;">
                    {format_number_with_commas(site_data['total_households'])}
                </div>
                <div style="font-size: 14px; color: rgba(255,255,255,0.8);">
                    Households
                </div>
            </div>
            <div style="text-align: center;">
                <div style="font-size: 28px; font-weight: 700; color: white; margin-bottom: 4px;">
                    {format_number_with_commas(site_data['total_measurements'])}
                </div>
                <div style="font-size: 14px; color: rgba(255,255,255,0.8);">
                    Measurements
                </div>
            </div>
            <div style="text-align: center;">
                <div style="font-size: 28px; font-weight: 700; color: white; margin-bottom: 4px;">
                    {format_percentage(site_data['stunting_rate'])}
                </div>
                <div style="font-size: 14px; color: rgba(255,255,255,0.8);">
                    Stunting Rate
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def create_ranking_card(title: str, value: str, rank: int, total: int, 
                       icon: str = "📊", color: str = COLORS['primary']) -> None:
    """
    Create a performance ranking card.
    
    Args:
        title: Card title
        value: Main value to display
        rank: Current rank
        total: Total number of sites
        icon: Icon emoji
        color: Card accent color
    """
    
    # Determine rank badge color and text
    if rank == 1:
        rank_color = "#FFD700"  # Gold
        rank_text = "🥇 1st"
    elif rank == 2:
        rank_color = "#C0C0C0"  # Silver
        rank_text = "🥈 2nd"
    elif rank == 3:
        rank_color = "#CD7F32"  # Bronze
        rank_text = "🥉 3rd"
    else:
        rank_color = COLORS['textSecondary']
        rank_text = f"#{rank}"
    
    # Use simple Streamlit components instead of complex HTML
    with st.container():
        st.markdown(f"**{icon} {title}**")
        st.metric(
            label="",
            value=value,
            delta=f"{rank_text} of {total}"
        )

def create_site_temporal_chart(data: pd.DataFrame) -> go.Figure:
    """
    Create temporal trends chart for selected site (Chart 1).
    
    Args:
        data: DataFrame with temporal data
    
    Returns:
        Plotly figure with dual y-axes
    """
    
    fig = make_subplots(
        rows=1, cols=1,
        specs=[[{"secondary_y": True}]]
    )
    
    # Add stunting rate line
    fig.add_trace(
        go.Scatter(
            x=data['period'],
            y=data['stunting_rate'],
            mode='lines+markers',
            line=dict(color=COLORS['stunted'], width=3),
            marker=dict(size=6),
            name='Stunting Rate %',
            yaxis='y'
        ),
        secondary_y=False,
    )
    
    # Add severe stunting rate line
    fig.add_trace(
        go.Scatter(
            x=data['period'],
            y=data['severe_stunting_rate'],
            mode='lines+markers',
            line=dict(color=COLORS['severelyStunted'], width=3),
            marker=dict(size=6),
            name='Severe Stunting %',
            yaxis='y'
        ),
        secondary_y=False,
    )
    
    # Add average z-score line
    fig.add_trace(
        go.Scatter(
            x=data['period'],
            y=data['avg_z_score'],
            mode='lines+markers',
            line=dict(color=COLORS['primary'], width=3),
            marker=dict(size=6),
            name='Avg Z-Score',
            yaxis='y2'
        ),
        secondary_y=True,
    )
    
    # Update layout
    fig.update_layout(
        title='Nutrition Outcomes Over Time',
        height=400,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color=COLORS['text']),
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    # Update axes
    fig.update_xaxes(
        gridcolor='#E2E8F0',
        linecolor='#718096',
        tickcolor='#718096',
        tickangle=-45
    )
    
    # Set y-axes titles
    fig.update_yaxes(
        title_text="Stunting Rate (%)",
        secondary_y=False,
        gridcolor='#E2E8F0',
        linecolor='#718096',
        tickcolor='#718096'
    )
    fig.update_yaxes(
        title_text="Average Z-Score",
        secondary_y=True,
        gridcolor='#E2E8F0',
        linecolor='#718096',
        tickcolor='#718096'
    )
    
    return fig

def create_site_status_distribution_chart(data: pd.DataFrame) -> go.Figure:
    """
    Create status distribution chart for selected site (Chart 3).
    
    Args:
        data: DataFrame with status distribution data
    
    Returns:
        Plotly figure
    """
    
    # Define colors for each status
    status_colors = {
        'Normal': COLORS['normal'],
        'At Risk': COLORS['atRisk'],
        'Stunted': COLORS['stunted'],
        'Severely Stunted': COLORS['severelyStunted']
    }
    
    colors = [status_colors.get(status, COLORS['primary']) for status in data['status']]
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=data['status'],
        y=data['count'],
        marker_color=colors,
        marker=dict(line=dict(width=0)),
        text=[f"{count}<br>({percentage}%)" for count, percentage in zip(data['count'], data['percentage'])],
        textposition='auto',
        hovertemplate='<b>%{x}</b><br>Count: %{y}<br>Percentage: %{text}<extra></extra>'
    ))
    
    fig.update_layout(
        title='Current Status Distribution',
        xaxis_title='Nutrition Status',
        yaxis_title='Number of Children',
        height=400,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color=COLORS['text']),
        showlegend=False
    )
    
    fig.update_xaxes(
        gridcolor='#E2E8F0',
        linecolor='#718096',
        tickcolor='#718096'
    )
    fig.update_yaxes(
        gridcolor='#E2E8F0',
        linecolor='#718096',
        tickcolor='#718096'
    )
    
    return fig

def create_z_score_comparison_chart(data: pd.DataFrame, selected_site: str) -> go.Figure:
    """
    Create z-score comparison chart across all sites (Chart 4).
    
    Args:
        data: DataFrame with z-score comparison data
        selected_site: Currently selected site
    
    Returns:
        Plotly figure
    """
    
    # Separate current site from others
    current_site_data = data[data['is_current'] == True]
    other_sites_data = data[data['is_current'] == False]
    
    fig = go.Figure()
    
    # Add other sites
    if not other_sites_data.empty:
        fig.add_trace(go.Bar(
            x=other_sites_data['children_count'],
            y=other_sites_data['site'],
            orientation='h',
            marker_color=COLORS['primary'],
            marker=dict(opacity=0.6, line=dict(width=0)),
            name='Other Sites',
            text=other_sites_data['avg_z_score'],
            textposition='auto',
            hovertemplate='<b>%{y}</b><br>Children: %{x}<br>Avg Z-Score: %{text}<extra></extra>'
        ))
    
    # Add current site (highlighted)
    if not current_site_data.empty:
        fig.add_trace(go.Bar(
            x=current_site_data['children_count'],
            y=current_site_data['site'],
            orientation='h',
            marker_color=COLORS['secondary'],
            marker=dict(line=dict(width=2, color='white')),
            name=f'{selected_site} (Selected)',
            text=current_site_data['avg_z_score'],
            textposition='auto',
            hovertemplate='<b>%{y}</b><br>Children: %{x}<br>Avg Z-Score: %{text}<extra></extra>'
        ))
    
    fig.update_layout(
        title='Z-Score Comparison Across Locations',
        xaxis_title='Number of Children',
        yaxis_title='',
        height=400,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color=COLORS['text']),
        showlegend=True
    )
    
    fig.update_xaxes(
        gridcolor='#E2E8F0',
        linecolor='#718096',
        tickcolor='#718096'
    )
    fig.update_yaxes(
        gridcolor='#E2E8F0',
        linecolor='#718096',
        tickcolor='#718096'
    )
    
    return fig

def create_stunting_comparison_chart(data: pd.DataFrame, selected_site: str) -> go.Figure:
    """
    Create stunting rate comparison chart across all sites (Chart 5).
    
    Args:
        data: DataFrame with stunting comparison data
        selected_site: Currently selected site
    
    Returns:
        Plotly figure
    """
    
    # Separate current site from others
    current_site_data = data[data['is_current'] == True]
    other_sites_data = data[data['is_current'] == False]
    
    fig = go.Figure()
    
    # Add other sites
    if not other_sites_data.empty:
        fig.add_trace(go.Bar(
            x=other_sites_data['stunting_rate'],
            y=other_sites_data['site'],
            orientation='h',
            marker_color=COLORS['stunted'],
            marker=dict(opacity=0.6, line=dict(width=0)),
            name='Other Sites',
            text=other_sites_data['stunting_rate'],
            textposition='auto',
            hovertemplate='<b>%{y}</b><br>Stunting Rate: %{x}%<extra></extra>'
        ))
    
    # Add current site (highlighted)
    if not current_site_data.empty:
        fig.add_trace(go.Bar(
            x=current_site_data['stunting_rate'],
            y=current_site_data['site'],
            orientation='h',
            marker_color=COLORS['severelyStunted'],
            marker=dict(line=dict(width=2, color='white')),
            name=f'{selected_site} (Selected)',
            text=current_site_data['stunting_rate'],
            textposition='auto',
            hovertemplate='<b>%{y}</b><br>Stunting Rate: %{x}%<extra></extra>'
        ))
    
    fig.update_layout(
        title='Stunting Rate Comparison Across Locations',
        xaxis_title='Stunting Rate (%)',
        yaxis_title='',
        height=400,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color=COLORS['text']),
        showlegend=True
    )
    
    fig.update_xaxes(
        gridcolor='#E2E8F0',
        linecolor='#718096',
        tickcolor='#718096'
    )
    fig.update_yaxes(
        gridcolor='#E2E8F0',
        linecolor='#718096',
        tickcolor='#718096'
    )
    
    return fig

def create_measurement_volume_chart(data: pd.DataFrame) -> go.Figure:
    """
    Create measurement volume over time chart (Chart 6).
    
    Args:
        data: DataFrame with measurement volume data
    
    Returns:
        Plotly figure
    """
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=data['period'],
        y=data['measurement_count'],
        mode='lines',
        fill='tonexty',
        fillcolor='rgba(102, 126, 234, 0.3)',  # Purple with opacity
        line=dict(color=COLORS['secondary'], width=3),
        name='Measurement Volume'
    ))
    
    fig.update_layout(
        title='Measurement Volume Over Time',
        xaxis_title='Quarter',
        yaxis_title='Number of Measurements',
        height=400,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color=COLORS['text']),
        showlegend=True
    )
    
    fig.update_xaxes(
        gridcolor='#E2E8F0',
        linecolor='#718096',
        tickcolor='#718096',
        tickangle=-45
    )
    fig.update_yaxes(
        gridcolor='#E2E8F0',
        linecolor='#718096',
        tickcolor='#718096'
    )
    
    return fig
