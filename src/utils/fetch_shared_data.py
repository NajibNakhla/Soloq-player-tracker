from src.api.get_puuid import get_puuid
from src.api.get_match_history import get_match_history
from src.api.get_match_details import get_match_details
from src.api.get_match_timeline import get_match_timeline
from src.utils.rate_tracker import check_rate_limit, update_rate_limit  # CHANGED: Import from our new tracker
from tqdm import tqdm
import time

def fetch_puuid_and_match_ids(region, game_name, tag_line, max_matches=1000):
    """Fetches PUUID and match IDs with rate limit awareness."""
    # Check rate limit before fetching PUUID
    sleep_time = check_rate_limit('account')
    if sleep_time > 0:
        print(f" Account API limit approaching. Sleeping for {sleep_time}s...")
        time.sleep(sleep_time)
    
    puuid, puuid_rate_info = get_puuid(region, game_name, tag_line)
    
    # Check rate limit before fetching match history
    sleep_time = check_rate_limit('match_history')
    if sleep_time > 0:
        print(f" Match history API limit approaching. Sleeping for {sleep_time}s...")
        time.sleep(sleep_time)
    
    match_ids, history_rate_info = get_match_history(region, puuid, max_matches)
    return puuid, match_ids

def fetch_match_and_timeline_data(region, match_ids, include_details=True, include_timeline=True, retries=2):
    """
    Fetches match and timeline data with proper rate limiting.
    """
    match_datas = []
    timeline_datas = []

    for match_id in tqdm(match_ids, desc="Fetching match & timeline data"):
        try:
            # Check rate limits before each API call
            if include_details:
                sleep_time = check_rate_limit('match')
                if sleep_time > 0:
                    print(f" Match API limit approaching. Sleeping for {sleep_time}s...")
                    time.sleep(sleep_time)
            
            if include_timeline:
                sleep_time = check_rate_limit('timeline')
                if sleep_time > 0:
                    print(f" Timeline API limit approaching. Sleeping for {sleep_time}s...")
                    time.sleep(sleep_time)

            if include_details:
                match_data, match_rate_info = get_match_details(region, match_id)
                if match_data:
                    match_datas.append((match_data, match_rate_info))  # CHANGED: Store tuple
                else:
                    print(f"Match data missing for {match_id}")

            if include_timeline:
                timeline_data, timeline_rate_info = get_match_timeline(region, match_id)
                if timeline_data and timeline_data.get("info", {}).get("frames"):
                    timeline_datas.append((timeline_data, timeline_rate_info))  # CHANGED: Store tuple
                else:
                    print(f"Timeline empty for {match_id}")
                    # Retry logic for empty timelines
                    for attempt in range(retries - 1):  # Already tried once
                        try:
                            time.sleep(1)  # Wait before retry
                            timeline_data, timeline_rate_info = get_match_timeline(region, match_id)
                            if timeline_data and timeline_data.get("info", {}).get("frames"):
                                timeline_datas.append((timeline_data, timeline_rate_info))
                                break
                        except Exception as e:
                            print(f"Retry {attempt+2} failed for timeline {match_id}: {e}")
                            continue

            # Minimal respectful sleep between matches
            time.sleep(0.1)

        except Exception as e:
            print(f"Error with match {match_id}: {e}")
            continue

    return match_datas, timeline_datas  # CHANGED: Now returns tuples with rate info

