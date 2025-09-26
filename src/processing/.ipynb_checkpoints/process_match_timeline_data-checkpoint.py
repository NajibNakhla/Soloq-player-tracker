def process_match_timeline(timeline_data: dict, target_puuid: str):
    """
    Extracts timeline-based metrics and spatial tracking for a specific player from a match timeline.

    Returns:
        metrics_dict (dict): key metrics across 5, 10, 15... up to match end
        positions_list (list): list of dicts for player position per minute
        wards_list (list): list of dicts for each ward placed (with position)
    """
    import math

    frames = timeline_data.get("info", {}).get("frames", [])
    events = []
    for frame in frames:
        events.extend(frame.get("events", []))

    # Map puuid to participantId
    puuid_to_pid = {entry["puuid"]: entry["participantId"] for entry in timeline_data.get("info", {}).get("participants", [])}
    pid = puuid_to_pid.get(target_puuid)
    if pid is None:
        return {}, [], []

    metrics = {"matchId": timeline_data.get("metadata", {}).get("matchId", "Unknown"), "puuid": target_puuid}


    # Dynamically compute valid timepoints (every 5 mins up to game end)
    max_minute = len(frames) - 1
    timepoints = [t for t in range(5, max_minute + 1, 5)]
    timestamp_limits = {t: t * 60000 for t in timepoints}
    metrics["matchDurationMin"] = max_minute                # Rounded down minute duration
    metrics["matchDurationMs"] = frames[-1].get("timestamp")  # Precise ms duration
    metrics["matchDurationExactMin"] = round(frames[-1].get("timestamp", 0) / 60000, 2)


    # Snapshot metrics per timepoint
    for t in timepoints:
        if t < len(frames):
            pdata = frames[t].get("participantFrames", {}).get(str(pid), {})
            metrics[f"goldAt{t}Min"] = pdata.get("totalGold")
            metrics[f"xpAt{t}Min"] = pdata.get("xp")
            metrics[f"levelAt{t}Min"] = pdata.get("level")
            metrics[f"csAt{t}Min"] = pdata.get("minionsKilled", 0) + pdata.get("jungleMinionsKilled", 0)
            metrics[f"jungleCSAt{t}Min"] = pdata.get("jungleMinionsKilled")
            metrics[f"allyJungleCSAt{t}Min"] = pdata.get("totalAllyJungleMinionsKilled")
            metrics[f"enemyJungleCSAt{t}Min"] = pdata.get("totalEnemyJungleMinionsKilled")
            pos = pdata.get("position", {})
            metrics[f"posXAt{t}Min"] = pos.get("x")
            metrics[f"posYAt{t}Min"] = pos.get("y")

    # Combat, vision, objective counters per timepoint
    counters = {t: {
        "kills": 0, "deaths": 0, "assists": 0, "soloKills": 0,
        "wardsPlaced": 0, "wardsKilled": 0, "controlWardsBought": 0,
        "plates": 0, "turrets": 0,
        "dragon": 0, "elder": 0, "baron": 0, "herald": 0,
        "voidGrub": 0, "voidScuttler": 0, "elite": 0
    } for t in timepoints}

    for event in events:
        ts = event.get("timestamp")
        if ts is None:
            continue

        for t in timepoints:
            if ts > timestamp_limits[t]:
                continue

            # Combat
            if event["type"] == "CHAMPION_KILL":
                if event.get("killerId") == pid:
                    counters[t]["kills"] += 1
                    if not event.get("assistingParticipantIds"):
                        counters[t]["soloKills"] += 1
                if event.get("victimId") == pid:
                    counters[t]["deaths"] += 1
                if pid in event.get("assistingParticipantIds", []):
                    counters[t]["assists"] += 1

            # Vision
            if event["type"] == "WARD_PLACED" and event.get("creatorId") == pid:
                counters[t]["wardsPlaced"] += 1
            if event["type"] == "WARD_KILL" and event.get("killerId") == pid:
                counters[t]["wardsKilled"] += 1
            if event["type"] == "ITEM_PURCHASED" and event.get("participantId") == pid:
                if event.get("itemId") == 2055:
                    counters[t]["controlWardsBought"] += 1

            # Objectives
            # Plate destruction event
            if event["type"] == "TURRET_PLATE_DESTROYED":
                if event.get("killerId") == pid:
                    counters[t]["plates"] += 1

            # Full tower destruction
            if event["type"] == "BUILDING_KILL":
                if event.get("buildingType") == "TOWER_BUILDING":
                    if event.get("killerId") == pid or pid in event.get("assistingParticipantIds", []):
                        counters[t]["turrets"] += 1


            if event["type"] == "ELITE_MONSTER_KILL":
                if event.get("killerId") == pid or pid in event.get("assistingParticipantIds", []):
                    mtype = event.get("monsterType", "")
                    if mtype == "DRAGON": counters[t]["dragon"] += 1
                    elif mtype == "ELDER_DRAGON": counters[t]["elder"] += 1
                    elif mtype == "BARON_NASHOR": counters[t]["baron"] += 1
                    elif mtype == "RIFTHERALD": counters[t]["herald"] += 1
                    elif mtype == "VOIDGRUB": counters[t]["voidGrub"] += 1
                    elif mtype == "VOIDSCUTTLER": counters[t]["voidScuttler"] += 1
                    counters[t]["elite"] += 1

    for t in timepoints:
        for k, v in counters[t].items():
            metrics[f"{k}At{t}Min"] = v
        kills = counters[t]['kills']
        deaths = counters[t]['deaths']
        assists = counters[t]['assists']
        metrics[f"kdaAt{t}Min"] = round((kills + assists) / max(1, deaths), 2)

    # One-time events
    def get_first_event(e_type, condition_fn):
        for e in events:
            if e.get("type") == e_type and condition_fn(e):
                return e.get("timestamp")
        return None

    def get_first_skill():
        for e in events:
            if e.get("type") == "SKILL_LEVEL_UP" and e.get("participantId") == pid:
                slot = e.get("skillSlot")
                return {1: "Q", 2: "W", 3: "E"}.get(slot)
        return None

    metrics["firstItemTime"] = get_first_event("ITEM_PURCHASED", lambda e: e.get("participantId") == pid)
    metrics["firstSkillUsed"] = get_first_skill()
    metrics["firstWardTime"] = get_first_event("WARD_PLACED", lambda e: e.get("creatorId") == pid)
    metrics["firstKillTime"] = get_first_event("CHAMPION_KILL", lambda e: e.get("killerId") == pid)
    metrics["firstDeathTime"] = get_first_event("CHAMPION_KILL", lambda e: e.get("victimId") == pid)

    # Position per minute
    positions = []
    for minute, frame in enumerate(frames):
        pdata = frame.get("participantFrames", {}).get(str(pid), {})
        pos = pdata.get("position")
        if pos:
            positions.append({
                "matchId": timeline_data.get("metadata", {}).get("matchId", "Unknown"),
                "puuid": target_puuid,
                "minute": minute,
                "x": pos.get("x"),
                "y": pos.get("y")
            })

    # Ward positions per minute
    # Ward positions (approximate via participant position at that time)
    wards = []
    for e in events:
        if e.get("type") == "WARD_PLACED" and e.get("creatorId") == pid:
            ts = e.get("timestamp", 0)
            minute = int(ts // 60000)
            if minute < len(frames):
                pdata = frames[minute]["participantFrames"].get(str(pid), {})
                pos = pdata.get("position", {})
                if pos:  # Make sure position exists
                    wards.append({
                        "matchId": timeline_data.get("metadata", {}).get("matchId", "Unknown"),
                        "puuid": target_puuid,
                        "timestamp": ts,
                        "minute": minute,
                        "wardType": e.get("wardType", "Unknown"),
                        "x": pos.get("x"),
                        "y": pos.get("y")
                    })


    return metrics, positions, wards
