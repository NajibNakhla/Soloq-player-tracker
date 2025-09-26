from .process_match_timeline_data import process_match_timeline

def process_multiple_timelines(timeline_list, target_puuid):
    """
    Processes multiple timeline dicts for a specific player using process_match_timeline.

    Args:
        timeline_list (list): List of timeline dicts (from Riot API)
        target_puuid (str): The player's PUUID to extract data for

    Returns:
        metrics_list (list of dict): Per-match timeline metrics
        all_positions (list of dict): All positional data across matches
        all_wards (list of dict): All ward placement data across matches
    """
    metrics_list = []
    all_positions = []
    all_wards = []

    for timeline_data in timeline_list:
        try:
            metrics, positions, wards = process_match_timeline(timeline_data, target_puuid)
            if metrics:
                metrics_list.append(metrics)
                all_positions.extend(positions)
                all_wards.extend(wards)
        except Exception as e:
            match_id = timeline_data.get("metadata", {}).get("matchId", "Unknown")
            print(f" Error processing timeline: {match_id} — {str(e)}")
            continue

    return metrics_list, all_positions, all_wards
