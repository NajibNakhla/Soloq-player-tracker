from src.pipelines.full_pipeline import run_full_pipeline
from src.database.connection import get_db_connection
from datetime import datetime, timedelta

def player_has_data(game_name: str, tag_line: str, max_age_hours: int = 24) -> bool:
    """Check if we have recent data for a player"""
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT MAX(processed_at) as last_update 
                FROM match_stats 
                WHERE puuid IN (
                    SELECT puuid FROM players 
                    WHERE game_name = %s AND tag_line = %s
                )
            """, (game_name, tag_line))
            
            result = cur.fetchone()
            if not result or not result[0]:
                return False  # No data at all
                
            # Check if data is fresh enough
            data_age = datetime.now() - result[0]
            return data_age < timedelta(hours=max_age_hours)
            
    finally:
        conn.close()

def ensure_player_data(region: str, game_name: str, tag_line: str, max_matches: int = 100):
    """
    Smart function: only runs pipeline if needed
    """
    # Check if we need fresh data
    if not player_has_data(game_name, tag_line):
        print(f" Fetching fresh data for {game_name}#{tag_line}")
        run_full_pipeline(region, game_name, tag_line, max_matches, save=True)
    else:
        print(f" Using existing data for {game_name}#{tag_line}")