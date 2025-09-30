"""
Reusable chart components for Streamlit.
"""

import plotly.express as px
import streamlit as st

def win_rate_metrics(winrate_data: dict, kda_data: dict):
    """Display win rate and KDA metrics with nice UI"""
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label="🎯 Total Games", 
            value=winrate_data['total_games'],
            delta=f"{winrate_data['wins']} Wins"
        )
    
    with col2:
        st.metric(
            label="🏆 Win Rate", 
            value=f"{winrate_data['win_rate']}%"
        )
    
    with col3:
        st.metric(
            label="⚔️ Average KDA", 
            value=kda_data['formatted_kda'],
            delta=f"{kda_data['kda_ratio']} Ratio"
        )

def side_performance_chart(side_data: list):
    """Bar chart for win rate by side"""
    if not side_data:
        st.info("No side data available")
        return
        
    fig = px.bar(side_data, x='side', y='win_rate', 
                title='Win Rate by Side', 
                color='side',
                color_discrete_map={'blue': '#1f77b4', 'red': '#d62728'})
    st.plotly_chart(fig, use_container_width=True)

def role_performance_chart(role_data: list):
    """Bar chart for win rate by role"""
    if not role_data:
        st.info("No role data available")
        return
        
    fig = px.bar(role_data, x='role', y='win_rate',
                title='Win Rate by Role',
                color='win_rate', 
                color_continuous_scale='Viridis')
    st.plotly_chart(fig, use_container_width=True)