import streamlit as st
from src.analytics.player_analytics import (
    get_player_overall_winrate, 
    get_winrate_by_side,
    get_winrate_by_role,
    get_player_average_kda
)
from src.api.get_puuid import get_puuid
from streamlit_app.components.charts.overview_charts import win_rate_metrics, side_performance_chart, role_performance_chart

def main():
    st.title("📊 Player Overview")
    
    # Check if player exists
    if 'current_player' not in st.session_state:
        st.warning("⚠️ Please collect player data first!")
        st.page_link("pages/1_Get_Player_Data.py", label="→ Go to Get Player Data")
        return
    
    # Get player from session state
    player = st.session_state.current_player
    st.success(f"📊 Analyzing: {player['game_name']}#{player['tag_line']}")
    
    # Get PUUID for analytics
    puuid, _ = get_puuid(player['region'], player['game_name'], player['tag_line'])
    
    # SECTION 1: Overall Performance
    st.header("🎯 Overall Performance")
    winrate_data = get_player_overall_winrate(puuid)
    kda_data = get_player_average_kda(puuid)
    win_rate_metrics(winrate_data, kda_data)
    
    # SECTION 2: Side Performance
    st.header("🔵🔴 Performance by Side")
    side_data = get_winrate_by_side(puuid)
    side_performance_chart(side_data)
    
    # SECTION 3: Role Performance  
    st.header("🎭 Performance by Role")
    role_data = get_winrate_by_role(puuid)
    role_performance_chart(role_data)

if __name__ == "__main__":
    main()