from src.processing.process_multiple_matches import process_multiple_matches
from src.utils.fetch_shared_data import fetch_puuid_and_match_ids, fetch_match_and_timeline_data
import pandas as pd
import os
from src.database.writer import save_match_stats

def run_player_pipeline(puuid, match_data_list, region, game_name, tag_line, max_matches=1000, save=True):
    # Process the data (unchanged)
    player_stats = process_multiple_matches(match_data_list, puuid)
    
    if save:
        # ONLY save to match_stats - matches and players are already saved
        save_match_stats(player_stats)
        print(f"  Saved {len(player_stats)} match stats to database")

    return player_stats