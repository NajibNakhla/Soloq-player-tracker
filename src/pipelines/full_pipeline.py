from src.pipelines.player_pipeline import run_player_pipeline
from src.pipelines.player_timeline_pipeline import run_player_timeline_pipeline
from src.utils.fetch_shared_data import fetch_puuid_and_match_ids, fetch_match_and_timeline_data
from src.database.writer import save_player, save_match  # ADD THESE IMPORTS
import traceback
import sys
sys.stdout.reconfigure(encoding='utf-8')

def run_full_pipeline(region: str, game_name: str, tag_line: str, max_matches: int = 400, save: bool = True):
    print(f" Starting full pipeline for {game_name}#{tag_line} ({max_matches} matches)")
    
    # Fetch PUUID and match IDs
    puuid, match_ids = fetch_puuid_and_match_ids(region, game_name, tag_line, max_matches)
    
    if save:
        # FIRST: Save player to players table (ONLY ONCE)
        save_player(puuid, game_name, tag_line, region)
        print(f"  Saved player {game_name}_{tag_line} to database")

    try:
        # Fetch match data for BOTH pipelines
        print("\n Fetching match and timeline data...")
        match_datas, timeline_datas = fetch_match_and_timeline_data(
            region, match_ids, include_details=True, include_timeline=True
        )
        
        if save:
            # SECOND: Save all matches to matches table (ONLY ONCE)
            for match_data, rate_info in match_datas:
                save_match(match_data,puuid)
            print(f"  Saved {len(match_datas)} matches to database")

        print("\n Running match-level pipeline...")
        # Extract just the data for processing
        match_data_list = [data for data, rate_info in match_datas]
        match_df = run_player_pipeline(puuid, match_data_list, region, game_name, tag_line, max_matches=max_matches, save=save)
        print(f" Match-level data collected: {len(match_df)} matches")

    except Exception as e:
        print(f" Failed during match pipeline: {e}")
        traceback.print_exc()
        return

    try:
        print("\n Running timeline-level pipeline...")
        # Extract just the timeline data for processing  
        timeline_data_list = [data for data, rate_info in timeline_datas]
        timeline_df, pos_df, ward_df = run_player_timeline_pipeline(
            puuid, timeline_data_list, region, game_name, tag_line, max_matches=max_matches, save=save
        )
        print(f" Timeline data collected: {len(timeline_df)} matches")

    except Exception as e:
        print(f" Failed during timeline pipeline: {e}")
        traceback.print_exc()
        return

    print("\n  All pipelines completed successfully.")




