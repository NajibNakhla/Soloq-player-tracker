# streamlit_app/main.py
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
    st.page_link("pages/1_🏠_Dashboard.py", label="Dashboard", icon="📊")
    st.page_link("pages/2_📊_Player_Analysis.py", label="Player Analysis", icon="👤")
    st.page_link("pages/3_📈_Match_Analysis.py", label="Match Analysis", icon="🔍")
    st.page_link("pages/4_⚙️_API_Status.py", label="API Status", icon="⚙️")
    
    st.divider()
    display_rate_limits()  # Shows rate limits in sidebar

# Main page content
st.title("Welcome to LoL Analyst!")
st.write("Use the sidebar to navigate to different analysis sections.")