def process_match_data(match_data: dict, target_puuid: str) -> dict:
    """
    Extracts detailed stats for a specific player from a match.

    Args:
        match_data (dict): Raw match data from Riot API.
        target_puuid (str): The player's PUUID.

    Returns:
        dict: A dictionary of all extracted stats (flat).
    """

    def safe_get(d: dict, *keys, default=None):
        for key in keys:
            d = d.get(key, {})
            if not isinstance(d, dict):
                return d
        return d if d else default

    info = match_data.get("info", {})
    match_id = match_data.get("metadata", {}).get("matchId", "Unknown")
    queue_id = info.get("queueId", 0)
    if queue_id != 420:
        return {}

        
    participants = info.get("participants", [])

    for p in participants:
        if p.get("puuid") == target_puuid:
            data = {"matchId": match_id, "puuid": target_puuid}
            
            #  Add enemy laner information
            position = p.get("individualPosition")
            team_id = p.get("teamId")
            enemy = next((e for e in participants if e.get("teamId") != team_id and e.get("individualPosition") == position), None)


            data["enemyChampion"] = enemy.get("championName") if enemy else "Unknown"
            data["enemyPuuid"] = enemy.get("puuid") if enemy else None
            data["enemyIndividualPosition"] = enemy.get("individualPosition") if enemy else N
            
            # 1. Identity & Context
            keys = [
                "championId", "championName", "individualPosition", "lane",
                "teamPosition"
            ]
            for k in keys:
                data[k] = p.get(k)

            # 2. Outcome
            data["win"] = p.get("win")
            data["gameEndedInSurrender"] = p.get("gameEndedInSurrender")
            data["gameEndedInEarlySurrender"] = p.get("gameEndedInEarlySurrender")

            # 3. Combat Performance
            combat_keys = [
                "kills", "deaths", "assists", "killingSprees", "doubleKills", "tripleKills", "quadraKills", "pentaKills",
                "firstBloodKill", "firstBloodAssist",
                "totalDamageDealtToChampions", "totalDamageDealt", "damageDealtToBuildings",
                "damageDealtToObjectives", "damageDealtToTurrets", "totalDamageTaken",
                "damageSelfMitigated", "magicDamageDealt", "magicDamageDealtToChampions",
                "magicDamageTaken", "physicalDamageDealt", "physicalDamageDealtToChampions",
                "physicalDamageTaken", "trueDamageDealt", "trueDamageDealtToChampions",
                "trueDamageTaken", "totalDamageShieldedOnTeammates", "totalHeal",
                "totalHealsOnTeammates", "totalTimeSpentDead", "longestTimeSpentLiving"
            ]
            for k in combat_keys:
                data[k] = p.get(k)

            challenge_combat = [
                "kda", "damagePerMinute", "teamDamagePercentage"
            ]
            for k in challenge_combat:
                data[f"challenges.{k}"] = safe_get(p, "challenges", k, default=0)

            # 4. Gold & Economy
            econ_keys = ["goldEarned", "goldSpent", "bountyLevel"]
            for k in econ_keys:
                data[k] = p.get(k)

            challenge_econ = ["goldPerMinute", "goldShare"]
            for k in challenge_econ:
                data[f"challenges.{k}"] = safe_get(p, "challenges", k, default=0)

            # 5. Farming
            farm_keys = [
                "totalMinionsKilled", "neutralMinionsKilled",
                "totalAllyJungleMinionsKilled", "totalEnemyJungleMinionsKilled"
            ]
            for k in farm_keys:
                data[k] = p.get(k)

            farm_challenges = [
                "csPerMinute", "maxCsAdvantageOnLaneOpponent", "jungleCsBefore10Minutes"
            ]
            for k in farm_challenges:
                data[f"challenges.{k}"] = safe_get(p, "challenges", k, default=0)

            # 6. Vision
            vision_keys = [
                "visionScore", "wardsPlaced", "wardsKilled",
                "visionWardsBoughtInGame", "sightWardsBoughtInGame"
            ]
            for k in vision_keys:
                data[k] = p.get(k)

            vision_challenges = [
                "visionScorePerMinute", "visionScoreAdvantageLaneOpponent",
                "wardTakedowns", "wardTakedownsBefore20M", "wardsGuarded",
                "stealthWardsPlaced"
            ]
            for k in vision_challenges:
                data[f"challenges.{k}"] = safe_get(p, "challenges", k, default=0)

            # 7. Objectives
            obj_keys = [
                "turretKills", "turretTakedowns", "turretsLost",
                "inhibitorKills", "inhibitorTakedowns", "inhibitorsLost",
                "baronKills", "dragonKills", "objectivesStolen", "objectivesStolenAssists",
                "firstTowerKill", "firstTowerAssist"
            ]
            for k in obj_keys:
                data[k] = p.get(k)

            obj_challenges = [
                "dragonTakedowns", "elderDragonMultikills", "elderDragonKillsWithOpposingSoul",
                "teamBaronKills", "teamElderDragonKills", "teamRiftHeraldKills",
                "riftHeraldTakedowns", "turretPlatesTaken", "turretsTakenWithRiftHerald",
                "firstTurretKilled", "firstTurretKilledTime", "quickFirstTurret"
            ]
            for k in obj_challenges:
                data[f"challenges.{k}"] = safe_get(p, "challenges", k, default=0)

            # 8. Pings
            ping_keys = [
                "onMyWayPings", "retreatPings", "getBackPings", "dangerPings",
                "enemyMissingPings", "enemyVisionPings", "pushPings", "commandPings",
                "needVisionPings", "visionClearedPings", "holdPings"
            ]
            for k in ping_keys:
                data[k] = p.get(k)

            # 9. Items
            for i in range(7):
                data[f"item{i}"] = p.get(f"item{i}", 0)
            data["itemsPurchased"] = p.get("itemsPurchased", 0)

            # 10. Misc / Utility
            misc_challenges = [
                "dodgeSkillShotsSmallWindow", "skillshotsHit", "tookLargeDamageSurvived",
                "pickKillWithAlly", "soloKills", "quickSoloKills", "unseenRecalls",
                "gameLength", "outnumberedKills", "earlyLaningPhaseGoldExpAdvantage",
                "effectiveHealAndShielding", "maxLevelLeadLaneOpponent", "takedowns",
                "takedownsAfterGainingLevelAdvantage", "takedownsBeforeJungleMinionSpawn",
                "hadOpenNexus", "voidMonsterKill"
            ]
            for k in misc_challenges:
                data[f"challenges.{k}"] = safe_get(p, "challenges", k, default=0)

            misc_keys = ["timePlayed", "champExperience", "champLevel"]
            for k in misc_keys:
                data[k] = p.get(k)

            return data

    return {}
