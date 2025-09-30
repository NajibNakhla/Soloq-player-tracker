import streamlit as st
from src.data.manager import ensure_player_data  # ← New import
from src.analytics.dashboard_queries import get_player_stats  # Your analysis functions

def main():
    st.title("Player Dashboard")
    
    # User input
    game_name = st.text_input("Game Name")
    tag_line = st.text_input("Tag Line")
    region = st.selectbox("Region", ["europe", "americas", "asia"])
    
    if st.button("Analyze") and game_name and tag_line:
        # STEP 1: Ensure data exists (this runs pipeline if needed)
        with st.spinner("Checking data availability..."):
            ensure_player_data(region, game_name, tag_line, max_matches=100)
        
        # STEP 2: Analyze from database (fast!)
        with st.spinner("Generating insights..."):
            results = get_player_stats(game_name, tag_line)
            display_results(results)