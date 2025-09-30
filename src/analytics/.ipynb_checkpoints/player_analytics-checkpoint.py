"""
Player analytics - queries, execution, and data preparation for charts.
"""

from src.database.connection import get_db_connection

def get_player_overall_winrate(puuid: str) -> dict:
    """
    Get overall win rate stats for a player.
    
    Returns: {'total_games': int, 'wins': int, 'win_rate': float}
    """
    query = """
        SELECT 
            COUNT(*) as total_games,
            SUM(CASE WHEN win THEN 1 ELSE 0 END) as wins,
            ROUND(AVG(CASE WHEN win THEN 1 ELSE 0 END) * 100, 2) as win_rate
        FROM match_stats 
        WHERE puuid = %s
    """
    
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(query, (puuid,))
            total_games, wins, win_rate = cur.fetchone()
            return {
                'total_games': total_games,
                'wins': wins,
                'win_rate': float(win_rate)
            }
    finally:
        conn.close()

def get_winrate_by_side(puuid: str) -> list:
    """
    Get win rate by side (blue/red).
    
    Returns: [{'side': 'blue', 'games': int, 'wins': int, 'win_rate': float}, ...]
    """
    query = """
        SELECT 
            side,
            COUNT(*) as games,
            SUM(CASE WHEN win THEN 1 ELSE 0 END) as wins,
            ROUND(AVG(CASE WHEN win THEN 1 ELSE 0 END) * 100, 2) as win_rate
        FROM match_stats 
        WHERE puuid = %s AND side IS NOT NULL
        GROUP BY side
        ORDER BY games DESC
    """
    
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(query, (puuid,))
            results = []
            for row in cur.fetchall():
                results.append({
                    'side': row[0],
                    'games': row[1],
                    'wins': row[2],
                    'win_rate': float(row[3])
                })
            return results
    finally:
        conn.close()

def get_winrate_by_role(puuid: str) -> list:
    """
    Get win rate by position/role.
    
    Returns: [{'role': 'TOP', 'games': int, 'win_rate': float}, ...]
    """
    query = """
        SELECT 
            individualposition as role,
            COUNT(*) as games,
            ROUND(AVG(CASE WHEN win THEN 1 ELSE 0 END) * 100, 2) as win_rate
        FROM match_stats 
        WHERE puuid = %s AND individualposition != ''
        GROUP BY individualposition
        ORDER BY games DESC
    """
    
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(query, (puuid,))
            results = []
            for row in cur.fetchall():
                results.append({
                    'role': row[0],
                    'games': row[1],
                    'win_rate': float(row[2])
                })
            return results
    finally:
        conn.close()

def get_recent_games(puuid: str, limit: int = 10) -> list:
    """
    Get most recent games for a player.
    
    Returns: List of recent matches with basic info
    """
    query = """
        SELECT 
            match_id,
            champion_name,
            win,
            kills,
            deaths,
            assists,
            side,
            individualposition
        FROM match_stats 
        WHERE puuid = %s
        ORDER BY match_id DESC
        LIMIT %s
    """
    
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(query, (puuid, limit))
            results = []
            for row in cur.fetchall():
                results.append({
                    'match_id': row[0],
                    'champion': row[1],
                    'win': row[2],
                    'kills': row[3],
                    'deaths': row[4],
                    'assists': row[5],
                    'side': row[6],
                    'role': row[7]
                })
            return results
    finally:
        conn.close()


def get_player_average_kda(puuid: str) -> dict:
    """
    Get average KDA stats for a player.
    
    Returns: {
        'avg_kills': float, 
        'avg_deaths': float, 
        'avg_assists': float,
        'kda_ratio': float,
        'formatted_kda': str
    }
    """
    query = """
        SELECT 
            ROUND(AVG(kills), 2) as avg_kills,
            ROUND(AVG(deaths), 2) as avg_deaths,
            ROUND(AVG(assists), 2) as avg_assists
        FROM match_stats 
        WHERE puuid = %s
    """
    
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(query, (puuid,))
            avg_kills, avg_deaths, avg_assists = cur.fetchone()
            
            # Calculate KDA ratio (standard formula: (kills + assists) / deaths)
            # Avoid division by zero
            if avg_deaths == 0:
                kda_ratio = avg_kills + avg_assists
            else:
                kda_ratio = round((avg_kills + avg_assists) / avg_deaths, 2)
            
            return {
                'avg_kills': float(avg_kills),
                'avg_deaths': float(avg_deaths),
                'avg_assists': float(avg_assists),
                'kda_ratio': kda_ratio,
                'formatted_kda': f"{avg_kills:.1f}/{avg_deaths:.1f}/{avg_assists:.1f}"
            }
    finally:
        conn.close()