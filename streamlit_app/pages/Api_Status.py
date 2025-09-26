# streamlit_app/pages/4_⚙️_API_Status.py
import streamlit as st
import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from src.utils.rate_tracker import get_rate_limit_info

st.title("⚙️ API Status & Rate Limits")

# Detailed rate limit view
st.header("Current Rate Limits")

api_types = ['account', 'match', 'match_history', 'timeline']
for api_type in api_types:
    info = get_rate_limit_info(api_type)
    
    col1, col2 = st.columns([1, 3])
    with col1:
        st.metric(
            label=f"{api_type.upper()} API",
            value=f"{info['used']}/{info['max']}",
            help=f"Used: {info['used']}, Limit: {info['max']}"
        )
    with col2:
        progress = info['used'] / info['max']
        st.progress(progress, text=f"{progress:.0%} utilized")

# Refresh button
if st.button("🔄 Refresh Rate Limits"):
    st.rerun()

# Explanation
st.info("""
**Rate Limit Information:**
- **Account API**: PUUID lookups
- **Match API**: Match details  
- **Match History**: Match ID lists
- **Timeline API**: Match timelines

*Rate limits reset every 2 minutes.*
""")