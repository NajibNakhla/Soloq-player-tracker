import streamlit as st
import requests
import time
from src.api.config import RIOT_API_KEY
from src.utils.rate_tracker import update_rate_limit

@st.cache_data(ttl=3600)  # Cache for 1 hour
def get_match_details(region: str, match_id: str) -> dict:
    """
    Fetches detailed match statistics for a given match ID.

    Args:
        region (str): Riot API region (e.g., "europe").
        match_id (str): Unique match ID (e.g., "EUW1_7313131872").

    Returns:
        dict: Match details (players, stats, win/loss, etc.) or empty dict if failed.
    """

    # Riot API endpoint for match details
    url = f"https://{region}.api.riotgames.com/lol/match/v5/matches/{match_id}"

    headers = {
        "X-Riot-Token": RIOT_API_KEY
    }
    rate_info = {"used": 0, "max": 20}


    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an error if request fails

        match_data = response.json()  # Full match details
        # Update rate-limit info from headers
        rate_info["used"] = int(response.headers.get("X-App-Rate-Limit-Count", "0:1").split(":")[0])
        rate_info["max"] = int(response.headers.get("X-App-Rate-Limit", "20:1").split(":")[0])
        update_rate_limit('match', rate_info['used'], rate_info['max'])
        return match_data ,rate_info

    except requests.exceptions.RequestException as e:
        print(f" Error fetching match details for {match_id}: {e}".encode('ascii', 'ignore').decode())
        return {}
