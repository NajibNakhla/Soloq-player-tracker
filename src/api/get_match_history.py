import streamlit as st
import requests
import time
from src.api.config import RIOT_API_KEY
from src.utils.rate_tracker import update_rate_limit


@st.cache_data(ttl=3600)  # Cache for 1 hour
def get_match_history(region: str, puuid: str, max_matches: int = 300) -> list:
    """
    Fetches up to 'max_matches' Solo Queue match IDs for a given player.

    Args:
        region (str): Riot API region (e.g., "europe").
        puuid (str): Player's unique PUUID.
        max_matches (int): Max number of matches to fetch (up to 100 per call).

    Returns:
        list: A list of match IDs (newest to oldest).
    """

    url = f"https://{region}.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids"
    headers = {"X-Riot-Token": RIOT_API_KEY}

    all_matches = []
    start = 0
    count = 100  # Max allowed per Riot API
    rate_info = {"used": 0, "max": 20}


    print(f" Fetching up to {max_matches} SoloQ match IDs for PUUID: {puuid}" .encode('ascii', 'ignore').decode())

    while len(all_matches) < max_matches:
        params = {
            "start": start,
            "count": min(count, max_matches - len(all_matches)),
            "type": "ranked",
            "queue": 420  # Solo Queue only
        }

        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            batch = response.json()

            if not batch:
                print(" No more matches found.")
                break

            all_matches.extend(batch)
            print(f" Retrieved {len(batch)} matches (Total: {len(all_matches)})".encode('ascii', 'ignore').decode())

            # Update rate-limit info from headers
            rate_info["used"] = int(response.headers.get("X-App-Rate-Limit-Count", "0:1").split(":")[0])
            rate_info["max"] = int(response.headers.get("X-App-Rate-Limit", "20:1").split(":")[0])


            start += len(batch)

            # Respect rate limit
            # time.sleep(1.1)
            update_rate_limit('match_history', rate_info['used'], rate_info['max'])

        except requests.exceptions.RequestException as e:
            print(f" Error fetching match history: {e}".encode('ascii', 'ignore').decode())
            break
            

    return all_matches, rate_info
