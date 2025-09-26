# src/utils/rate_tracker.py
import streamlit as st
import time
from datetime import datetime

def init_rate_tracker():
    """Initialize rate limit tracker in session state."""
    if 'rate_limits' not in st.session_state:
        st.session_state.rate_limits = {
            'account': {'used': 0, 'max': 20, 'last_update': time.time()},
            'match': {'used': 0, 'max': 20, 'last_update': time.time()},
            'match_history': {'used': 0, 'max': 20, 'last_update': time.time()},
            'timeline': {'used': 0, 'max': 20, 'last_update': time.time()}
        }

def update_rate_limit(api_type, used_count, max_count):
    """Update rate limit information for a specific API type."""
    init_rate_tracker()
    
    st.session_state.rate_limits[api_type] = {
        'used': used_count,
        'max': max_count,
        'last_update': time.time(),
        'updated_at': datetime.now().strftime("%H:%M:%S")
    }

def get_rate_limit_info(api_type):
    """Get current rate limit information for an API type."""
    init_rate_tracker()
    return st.session_state.rate_limits.get(api_type, {'used': 0, 'max': 20})

def check_rate_limit(api_type, threshold=0.8):
    """
    Check if we're approaching rate limit and return recommended sleep time.
    Returns: sleep_time (0 if no sleep needed)
    """
    info = get_rate_limit_info(api_type)
    remaining = info['max'] - info['used']
    
    if info['used'] >= (info['max'] * threshold):
        return 10  # Long sleep if close to limit
    elif remaining <= 3:
        return 2   # Short sleep if very few left
    elif remaining <= 5:
        return 1   # Brief pause if getting low
    return 0       # No sleep needed

def display_rate_limits():
    """Display current rate limits in Streamlit sidebar."""
    init_rate_tracker()
    
    st.sidebar.subheader("📊 API Rate Limits")
    for api_type, info in st.session_state.rate_limits.items():
        progress = info['used'] / info['max']
        color = "red" if progress > 0.8 else "orange" if progress > 0.6 else "green"
        
        st.sidebar.progress(
            progress, 
            text=f"{api_type.upper()}: {info['used']}/{info['max']} (Updated: {info.get('updated_at', 'N/A')})"
        )