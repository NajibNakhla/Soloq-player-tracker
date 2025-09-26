import streamlit as st
import requests
from src.utils.rate_tracker import update_rate_limit

# Load API Key from a config file (better security)
from src.api.config import RIOT_API_KEY

@st.cache_data(ttl=3600)  # Cache for 1 hour
def get_puuid(region: str, game_name: str, tag_line: str):
    """
    Fetches the PUUID (Player Unique ID) from Riot API using game name and tagline.
    
    Args:
        region (str): Riot API region (e.g., "europe").
        game_name (str): Player's in-game name (e.g., "Nakla").
        tag_line (str): Player's tagline (e.g., "EUW").

    Returns:
        tuple:
            - str: PUUID if found, else None
            - dict: rate-limit info {'used': int, 'max': int} or None
    """

    url = f"https://{region}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{game_name}/{tag_line}"
    headers = {"X-Riot-Token": RIOT_API_KEY}
    rate_info = {"used": 0, "max": 20}


    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        # Extract PUUID
        data = response.json()
        puuid = data["puuid"]

        # Extract rate-limit info from headers
        rate_info = {
            "used": int(response.headers.get("X-App-Rate-Limit-Count", "0:1").split(":")[0]),
            "max": int(response.headers.get("X-App-Rate-Limit", "20:1").split(":")[0])
        }

        update_rate_limit('account', rate_info['used'], rate_info['max'])

        return puuid, rate_info

    except requests.exceptions.RequestException as e:
        print(f"Error fetching PUUID: {e}".encode('ascii', 'ignore').decode())
        return None, None
