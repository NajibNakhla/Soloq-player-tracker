from .process_match_data import process_match_data

def process_multiple_matches(match_datas: list, puuid: str) -> list:
    """
    Processes multiple match data objects for a specific player and returns a list of match-level stats.

    Args:
        match_datas (list): A list of raw match data dicts (already fetched via API).
        puuid (str): The player's PUUID.

    Returns:
        list: A list of dictionaries, each containing that player's stats for one match.
    """
    all_stats = []

    for match_data in match_datas:
        try:
            if not match_data:
                continue

            player_stats = process_match_data(match_data, target_puuid=puuid)
            if player_stats:
                all_stats.append(player_stats)

        except Exception as e:
            print(f" Skipped a match due to error: {e}")
            continue

    return all_stats
