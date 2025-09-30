import streamlit as st
import sys
import os

# Add src to path so we can import your modules
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.utils.rate_tracker import init_rate_tracker, display_rate_limits

# Initialize rate tracker
init_rate_tracker()

# Page configuration
st.set_page_config(
    page_title="LoL Analyst",
    page_icon="🎮", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Display rate limits in sidebar
with st.sidebar:
    st.title("🎮 LoL Analyst")
    st.page_link("main.py", label="Home", icon="🏠")
    st.page_link("pages/1_Get_Player_Data.py", label="Get Player Data", icon="📥")
    
    # ✅ CONDITIONALLY SHOW ANALYSIS PAGES
    if 'current_player' in st.session_state:
        player = st.session_state.current_player
        st.success(f"👤 {player['game_name']}#{player['tag_line']}")
        
        # Show analysis pages
        st.page_link("pages/2_Player_Overview.py", label="Player Overview", icon="📊")
        # st.page_link("pages/3_🔍_Match_Analysis.py", label="Match Analysis", icon="🔍")
        # st.page_link("pages/4_⚙️_API_Status.py", label="API Status", icon="⚙️")
    else:
        st.warning("⏳ No player data collected")
    
    st.divider()
    display_rate_limits()  # Shows rate limits in sidebar

# Main page content
st.title("Welcome to LoL Analyst!")
st.write("Use the sidebar to navigate to different analysis sections.")

# Add instructions for the new flow
st.info("""
**Getting Started:**
1. **📥 Get Player Data** - First, collect your match data from Riot API
2. **📊 Player Overview** - Then, view insights and charts from your data
3. **🔍 Match Analysis** - Dive deep into individual matches (coming soon)
""")

# ✅ Show current player status on home page
if 'current_player' in st.session_state:
    player = st.session_state.current_player
    st.success(f"✅ Currently analyzing: **{player['game_name']}#{player['tag_line']}**")
    st.page_link("pages/2_Player_Overview.py", label="→ Go to Player Overview", icon="📊")