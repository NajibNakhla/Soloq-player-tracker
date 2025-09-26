from src.processing.process_multiple_timelines import process_multiple_timelines
from src.utils.fetch_shared_data import fetch_puuid_and_match_ids, fetch_match_and_timeline_data
import pandas as pd
import os
from src.database.writer import save_timeline_metrics  # Import the new database writer

def run_player_timeline_pipeline(puuid, timeline_data_list, region, game_name, tag_line, max_matches=1000, save=True):
    # Process the data (unchanged)
    metrics_list, positions_list, wards_list = process_multiple_timelines(timeline_data_list, puuid)

    if save:
        # ONLY save timeline data - matches and players are already saved
        save_timeline_metrics(metrics_list)
        print(f" ✅ Saved {len(metrics_list)} timeline metrics to database")

    return metrics_list, positions_list, wards_list