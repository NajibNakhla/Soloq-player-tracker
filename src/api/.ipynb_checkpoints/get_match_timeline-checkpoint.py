import streamlit as st
import requests
import time
from src.api.config import RIOT_API_KEY

@st.cache_data(ttl=3600)  # Cache for 1 hour
def get_match_timeline(region: str, match_id: str) -> dict:
    """
    Fetches the detailed timeline for a given match ID.

    Args:
        region (str): Riot API region (e.g., "europe").
        match_id (str): Unique match ID (e.g., "EUW1_7313131872").

    Returns:
        dict: Match timeline data or empty dict if failed.
    """

    # Riot API endpoint for match timeline
    url = f"https://{region}.api.riotgames.com/lol/match/v5/matches/{match_id}/timeline"

    headers = {
        "X-Riot-Token": RIOT_API_KEY
    }
    rate_info = {"used": 0, "max": 20}


    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise error if request fails

        timeline_data = response.json()  # Full match timeline
        # Update rate-limit info from headers
        rate_info["used"] = int(response.headers.get("X-App-Rate-Limit-Count", "0:1").split(":")[0])
        rate_info["max"] = int(response.headers.get("X-App-Rate-Limit", "20:1").split(":")[0])
        return timeline_data ,rate_info

    except requests.exceptions.RequestException as e:
        print(f" Error fetching match timeline for {match_id}: {e}".encode('ascii', 'ignore').decode())
        return {}
