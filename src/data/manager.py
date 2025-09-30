from src.pipelines.full_pipeline import run_full_pipeline
from src.database.connection import get_db_connection
from datetime import datetime, timedelta

def player_has_data(game_name: str, tag_line: str, max_age_hours: int = 24) -> bool:
    """Check if we have recent data for a player"""
    # TEMPORARY: Always return False to force data collection
    return False  # ← This will make it always fetch fresh data
    
    # Comment out the rest for now:
    """
    to update later 
    """

def ensure_player_data(region: str, game_name: str, tag_line: str, max_matches: int = 100):
    """
    Smart function: only runs pipeline if needed
    """
    # Check if we need fresh data
    if not player_has_data(game_name, tag_line):
        print(f"🔄 Fetching fresh data for {game_name}#{tag_line}")
        run_full_pipeline(region, game_name, tag_line, max_matches, save=True)
    else:
        print(f"✅ Using existing data for {game_name}#{tag_line}")