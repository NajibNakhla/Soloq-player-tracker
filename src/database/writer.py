# src/database/writer.py
from .connection import get_db_connection
import json


def save_match(match_data, player_puuid):
    """
    Saves basic match information to the matches table.
    """
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            # Extract basic match info - USE YOUR ACTUAL COLUMNS
            match_info = match_data.get('info', {})
            mapped_data = {
                'match_id': match_data.get('metadata', {}).get('matchId'),
                'puuid': player_puuid,  # ← ADD THIS REQUIRED FIELD
                'queue_id': match_info.get('queueId'),
                'game_length': match_info.get('gameDuration'),  # ← CORRECT COLUMN NAME
                # Add other columns you have: win, game_ended_in_surrender, etc.
            }
            
            # Filter out None values
            mapped_data = {k: v for k, v in mapped_data.items() if v is not None}
            
            columns = ', '.join(mapped_data.keys())
            placeholders = ', '.join([f'%({key})s' for key in mapped_data.keys()])
            
            cur.execute(f"""
                INSERT INTO matches ({columns})
                VALUES ({placeholders})
                ON CONFLICT (match_id) DO NOTHING
            """, mapped_data)
        
        conn.commit()
    except Exception as e:
        conn.rollback()
        print(f" Error saving match: {e}")
        raise
    finally:
        conn.close()

def save_player(player_puuid, game_name=None, tag_line=None, region=None):
    """
    Saves basic player information to the players table.
    """
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            mapped_data = {
                'puuid': player_puuid,
                'game_name': game_name,
                'tag_line': tag_line,
                'region': region,
                
            }
            
            # Filter out None values
            mapped_data = {k: v for k, v in mapped_data.items() if v is not None}
            
            columns = ', '.join(mapped_data.keys())
            placeholders = ', '.join([f'%({key})s' for key in mapped_data.keys()])
            
            cur.execute(f"""
                INSERT INTO players ({columns})
                VALUES ({placeholders})
                ON CONFLICT (puuid) DO NOTHING
            """, mapped_data)
        
        conn.commit()
    except Exception as e:
        conn.rollback()
        print(f" Error saving player: {e}")
        raise
    finally:
        conn.close()

def save_match_stats(stats_list):
    """
    Takes a list of match stat dicts (with camelCase keys from API) 
    and inserts them into the match_stats table.
    """
    if not stats_list:
        print(" No match stats to save.")
        return

    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            for stats in stats_list:
                # Map camelCase API keys to snake_case database columns
                mapped_data = {
                    # Identifiers and Metadata
                    'match_id': stats.get('matchId'),
                    'puuid': stats.get('puuid'),
                    'enemychampion': stats.get('enemyChampion'),
                    'enemypuuid': stats.get('enemyPuuid'),
                    'enemyindividualposition': stats.get('enemyIndividualPosition'),
                    'championid': stats.get('championId'),
                    'championname': stats.get('championName'),
                    'individualposition': stats.get('individualPosition'),
                    'lane': stats.get('lane'),
                    'teamposition': stats.get('teamPosition'),
                    
                    # Match Outcome
                    'win': stats.get('win'),
                    'gameendedinsurrender': stats.get('gameEndedInSurrender'),
                    'gameendedinearlysurrender': stats.get('gameEndedInEarlySurrender'),
                    
                    # Core Stats
                    'kills': stats.get('kills'),
                    'deaths': stats.get('deaths'),
                    'assists': stats.get('assists'),
                    'killingsprees': stats.get('killingSprees'),
                    'doublekills': stats.get('doubleKills'),
                    'triplekills': stats.get('tripleKills'),
                    'quadrakills': stats.get('quadraKills'),
                    'pentakills': stats.get('pentaKills'),
                    'firstbloodkill': stats.get('firstBloodKill'),
                    'firstbloodassist': stats.get('firstBloodAssist'),
                    
                    # Damage Stats
                    'totaldamagedealttochampions': stats.get('totalDamageDealtToChampions'),
                    'totaldamagedealt': stats.get('totalDamageDealt'),
                    'damagedealttobuildings': stats.get('damageDealtToBuildings'),
                    'damagedealttoobjectives': stats.get('damageDealtToObjectives'),
                    'damagedealttoturrets': stats.get('damageDealtToTurrets'),
                    'totaldamagetaken': stats.get('totalDamageTaken'),
                    'damageselfmitigated': stats.get('damageSelfMitigated'),
                    'magicdamagedealt': stats.get('magicDamageDealt'),
                    'magicdamagedealttochampions': stats.get('magicDamageDealtToChampions'),
                    'magicdamagetaken': stats.get('magicDamageTaken'),
                    'physicaldamagedealt': stats.get('physicalDamageDealt'),
                    'physicaldamagedealttochampions': stats.get('physicalDamageDealtToChampions'),
                    'physicaldamagetaken': stats.get('physicalDamageTaken'),
                    'truedamagedealt': stats.get('trueDamageDealt'),
                    'truedamagedealttochampions': stats.get('trueDamageDealtToChampions'),
                    'truedamagetaken': stats.get('trueDamageTaken'),
                    'totaldamageshieldedonteammates': stats.get('totalDamageShieldedOnTeammates'),
                    
                    # Healing and Survival
                    'totalheal': stats.get('totalHeal'),
                    'totalhealsonteammates': stats.get('totalHealsOnTeammates'),
                    'totaltimespentdead': stats.get('totalTimeSpentDead'),
                    'longesttimespentliving': stats.get('longestTimeSpentLiving'),
                    
                    # Challenges
                    'challenges_kda': stats.get('challenges.kda'),
                    'challenges_damageperminute': stats.get('challenges.damagePerMinute'),
                    'challenges_teamdamagepercentage': stats.get('challenges.teamDamagePercentage'),
                    
                    # Gold and Economy
                    'goldearned': stats.get('goldEarned'),
                    'goldspent': stats.get('goldSpent'),
                    'bountylevel': stats.get('bountyLevel'),
                    'challenges_goldperminute': stats.get('challenges.goldPerMinute'),
                    'challenges_goldshare': stats.get('challenges.goldShare'),
                    
                    # Minions and CS
                    'totalminionskilled': stats.get('totalMinionsKilled'),
                    'neutralminionskilled': stats.get('neutralMinionsKilled'),
                    'totalallyjungleminionskilled': stats.get('totalAllyJungleMinionsKilled'),
                    'totalenemyjungleminionskilled': stats.get('totalEnemyJungleMinionsKilled'),
                    'challenges_csperminute': stats.get('challenges.csPerMinute'),
                    'challenges_maxcsadvantageonlaneopponent': stats.get('challenges.maxCsAdvantageOnLaneOpponent'),
                    'challenges_junglecsbefore10minutes': stats.get('challenges.jungleCsBefore10Minutes'),
                    
                    # Vision
                    'visionscore': stats.get('visionScore'),
                    'wardsplaced': stats.get('wardsPlaced'),
                    'wardskilled': stats.get('wardsKilled'),
                    'visionwardsboughtingame': stats.get('visionWardsBoughtInGame'),
                    'sightwardsboughtingame': stats.get('sightWardsBoughtInGame'),
                    'challenges_visionscoreperminute': stats.get('challenges.visionScorePerMinute'),
                    'challenges_visionscoreadvantagelaneopponent': stats.get('challenges.visionScoreAdvantageLaneOpponent'),
                    'challenges_wardtakedowns': stats.get('challenges.wardTakedowns'),
                    'challenges_wardtakedownsbefore20m': stats.get('challenges.wardTakedownsBefore20M'),
                    'challenges_wardsguarded': stats.get('challenges.wardsGuarded'),
                    'challenges_stealthwardsplaced': stats.get('challenges.stealthWardsPlaced'),
                    
                    # Objectives
                    'turretkills': stats.get('turretKills'),
                    'turrettakedowns': stats.get('turretTakedowns'),
                    'turretslost': stats.get('turretsLost'),
                    'inhibitorkills': stats.get('inhibitorKills'),
                    'inhibitortakedowns': stats.get('inhibitorTakedowns'),
                    'inhibitorslost': stats.get('inhibitorsLost'),
                    'baronkills': stats.get('baronKills'),
                    'dragonkills': stats.get('dragonKills'),
                    'objectivesstolen': stats.get('objectivesStolen'),
                    'objectivesstolenassists': stats.get('objectivesStolenAssists'),
                    'firsttowerkill': stats.get('firstTowerKill'),
                    'firsttowerassist': stats.get('firstTowerAssist'),
                    'challenges_dragontakedowns': stats.get('challenges.dragonTakedowns'),
                    'challenges_elderdragonmultikills': stats.get('challenges.elderDragonMultikills'),
                    'challenges_elderdragonkillswithopposingsoul': stats.get('challenges.elderDragonKillsWithOpposingSoul'),
                    'challenges_teambaronkills': stats.get('challenges.teamBaronKills'),
                    'challenges_teamelderdragonkills': stats.get('challenges.teamElderDragonKills'),
                    'challenges_teamriftheraldkills': stats.get('challenges.teamRiftHeraldKills'),
                    'challenges_riftheraldtakedowns': stats.get('challenges.riftHeraldTakedowns'),
                    'challenges_turretplatestaken': stats.get('challenges.turretPlatesTaken'),
                    'challenges_turretstakenwithriftherald': stats.get('challenges.turretsTakenWithRiftHerald'),
                    'challenges_firstturretkilled': stats.get('challenges.firstTurretKilled'),
                    'challenges_firstturretkilledtime': stats.get('challenges.firstTurretKilledTime'),
                    'challenges_quickfirstturret': stats.get('challenges.quickFirstTurret'),
                    
                    # Pings
                    'onmywaypings': stats.get('onMyWayPings'),
                    'retreatpings': stats.get('retreatPings'),
                    'getbackpings': stats.get('getBackPings'),
                    'dangerpings': stats.get('dangerPings'),
                    'enemymissingpings': stats.get('enemyMissingPings'),
                    'enemyvisionpings': stats.get('enemyVisionPings'),
                    'pushpings': stats.get('pushPings'),
                    'commandpings': stats.get('commandPings'),
                    'needvisionpings': stats.get('needVisionPings'),
                    'visionclearedpings': stats.get('visionClearedPings'),
                    'holdpings': stats.get('holdPings'),
                    
                    # Items
                    'item0': stats.get('item0'),
                    'item1': stats.get('item1'),
                    'item2': stats.get('item2'),
                    'item3': stats.get('item3'),
                    'item4': stats.get('item4'),
                    'item5': stats.get('item5'),
                    'item6': stats.get('item6'),
                    'itemspurchased': stats.get('itemsPurchased'),
                    
                    # More Challenges
                    'challenges_dodgeskillshotssmallwindow': stats.get('challenges.dodgeSkillShotsSmallWindow'),
                    'challenges_skillshotshit': stats.get('challenges.skillshotsHit'),
                    'challenges_tooklargedamagesurvived': stats.get('challenges.tookLargeDamageSurvived'),
                    'challenges_pickkillwithally': stats.get('challenges.pickKillWithAlly'),
                    'challenges_solokills': stats.get('challenges.soloKills'),
                    'challenges_quicksolokills': stats.get('challenges.quickSoloKills'),
                    'challenges_unseenrecalls': stats.get('challenges.unseenRecalls'),
                    'challenges_gamelength': stats.get('challenges.gameLength'),
                    'challenges_outnumberedkills': stats.get('challenges.outnumberedKills'),
                    'challenges_earlylaningphasegoldexpadvantage': stats.get('challenges.earlyLaningPhaseGoldExpAdvantage'),
                    'challenges_effectivehealandshielding': stats.get('challenges.effectiveHealAndShielding'),
                    'challenges_maxlevelleadlaneopponent': stats.get('challenges.maxLevelLeadLaneOpponent'),
                    'challenges_takedowns': stats.get('challenges.takedowns'),
                    'challenges_takedownsaftergainingleveladvantage': stats.get('challenges.takedownsAfterGainingLevelAdvantage'),
                    'challenges_takedownsbeforejungleminionspawn': stats.get('challenges.takedownsBeforeJungleMinionSpawn'),
                    'challenges_hadopennexus': stats.get('challenges.hadOpenNexus'),
                    'challenges_voidmonsterkill': stats.get('challenges.voidMonsterKill'),
                    
                    # Experience and Time
                    'timeplayed': stats.get('timePlayed'),
                    'champexperience': stats.get('champExperience'),
                    'champlevel': stats.get('champLevel'),
                }
                
                # Filter out None values to avoid database errors
                mapped_data = {k: v for k, v in mapped_data.items() if v is not None}
                
                # Create the SQL query dynamically based on available keys
                columns = ', '.join(mapped_data.keys())
                placeholders = ', '.join([f'%({key})s' for key in mapped_data.keys()])
                
                cur.execute(f"""
                    INSERT INTO match_stats ({columns})
                    VALUES ({placeholders})
                    ON CONFLICT (match_id, puuid) DO NOTHING
                """, mapped_data)
        
        conn.commit()
        print(f" Successfully saved {len(stats_list)} match stats to database.")
        
    except Exception as e:
        conn.rollback()
        print(f" Error saving match stats: {e}")
        raise
    finally:
        conn.close()



def save_timeline_metrics(metrics_list):
    """
    Takes timeline metrics with camelCase keys and inserts them into match_timelines table.
    """
    if not metrics_list:
        print(" No timeline metrics to save.")
        return

    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            for metrics in metrics_list:
                mapped_data = {
                    'match_id': metrics.get('matchId'),
                    'puuid': metrics.get('puuid'),
                    'match_duration_min': metrics.get('matchDurationMin'),
                    'champion_name': metrics.get('championName'),
                    'individual_position': metrics.get('individualPosition'),
                    'timeline_data': metrics  # The entire camelCase dictionary as JSON
                }
                
                # Filter out None values
                mapped_data = {k: v for k, v in mapped_data.items() if v is not None}
                
                cur.execute("""
                    INSERT INTO match_timelines 
                    (match_id, puuid, match_duration_min, champion_name, individual_position, timeline_data)
                    VALUES (%(match_id)s, %(puuid)s, %(match_duration_min)s, 
                            %(champion_name)s, %(individual_position)s, %(timeline_data)s)
                    ON CONFLICT (match_id, puuid) DO NOTHING
                """, mapped_data)
        
        conn.commit()
        print(f" Successfully saved {len(metrics_list)} timeline metrics to database.")
        
    except Exception as e:
        conn.rollback()
        print(f" Error saving timeline metrics: {e}")
        raise
    finally:
        conn.close()

# src/database/writer.py
from .connection import get_db_connection


def save_match(match_data, player_puuid):
    """
    Saves basic match information to the matches table.
    """
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            # Extract basic match info - USE YOUR ACTUAL COLUMNS
            match_info = match_data.get('info', {})
            mapped_data = {
                'match_id': match_data.get('metadata', {}).get('matchId'),
                'puuid': player_puuid,  # ← ADD THIS REQUIRED FIELD
                'queue_id': match_info.get('queueId'),
                'game_length': match_info.get('gameDuration'),  # ← CORRECT COLUMN NAME
                # Add other columns you have: win, game_ended_in_surrender, etc.
            }
            
            # Filter out None values
            mapped_data = {k: v for k, v in mapped_data.items() if v is not None}
            
            columns = ', '.join(mapped_data.keys())
            placeholders = ', '.join([f'%({key})s' for key in mapped_data.keys()])
            
            cur.execute(f"""
                INSERT INTO matches ({columns})
                VALUES ({placeholders})
                ON CONFLICT (match_id) DO NOTHING
            """, mapped_data)
        
        conn.commit()
    except Exception as e:
        conn.rollback()
        print(f" Error saving match: {e}")
        raise
    finally:
        conn.close()

def save_player(player_puuid, game_name=None, tag_line=None, region=None):
    """
    Saves basic player information to the players table.
    """
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            mapped_data = {
                'puuid': player_puuid,
                'game_name': game_name,
                'tag_line': tag_line,
                'region': region,
                
            }
            
            # Filter out None values
            mapped_data = {k: v for k, v in mapped_data.items() if v is not None}
            
            columns = ', '.join(mapped_data.keys())
            placeholders = ', '.join([f'%({key})s' for key in mapped_data.keys()])
            
            cur.execute(f"""
                INSERT INTO players ({columns})
                VALUES ({placeholders})
                ON CONFLICT (puuid) DO NOTHING
            """, mapped_data)
        
        conn.commit()
    except Exception as e:
        conn.rollback()
        print(f" Error saving player: {e}")
        raise
    finally:
        conn.close()

def save_match_stats(stats_list):
    """
    Takes a list of match stat dicts (with camelCase keys from API) 
    and inserts them into the match_stats table.
    """
    if not stats_list:
        print(" No match stats to save.")
        return

    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            for stats in stats_list:
                # Map camelCase API keys to snake_case database columns
                mapped_data = {
                    # Identifiers and Metadata
                    'match_id': stats.get('matchId'),
                    'puuid': stats.get('puuid'),
                    'enemychampion': stats.get('enemyChampion'),
                    'enemypuuid': stats.get('enemyPuuid'),
                    'enemyindividualposition': stats.get('enemyIndividualPosition'),
                    'championid': stats.get('championId'),
                    'championname': stats.get('championName'),
                    'individualposition': stats.get('individualPosition'),
                    'lane': stats.get('lane'),
                    'teamposition': stats.get('teamPosition'),
                    
                    # Match Outcome
                    'win': stats.get('win'),
                    'gameendedinsurrender': stats.get('gameEndedInSurrender'),
                    'gameendedinearlysurrender': stats.get('gameEndedInEarlySurrender'),
                    
                    # Core Stats
                    'kills': stats.get('kills'),
                    'deaths': stats.get('deaths'),
                    'assists': stats.get('assists'),
                    'killingsprees': stats.get('killingSprees'),
                    'doublekills': stats.get('doubleKills'),
                    'triplekills': stats.get('tripleKills'),
                    'quadrakills': stats.get('quadraKills'),
                    'pentakills': stats.get('pentaKills'),
                    'firstbloodkill': stats.get('firstBloodKill'),
                    'firstbloodassist': stats.get('firstBloodAssist'),
                    
                    # Damage Stats
                    'totaldamagedealttochampions': stats.get('totalDamageDealtToChampions'),
                    'totaldamagedealt': stats.get('totalDamageDealt'),
                    'damagedealttobuildings': stats.get('damageDealtToBuildings'),
                    'damagedealttoobjectives': stats.get('damageDealtToObjectives'),
                    'damagedealttoturrets': stats.get('damageDealtToTurrets'),
                    'totaldamagetaken': stats.get('totalDamageTaken'),
                    'damageselfmitigated': stats.get('damageSelfMitigated'),
                    'magicdamagedealt': stats.get('magicDamageDealt'),
                    'magicdamagedealttochampions': stats.get('magicDamageDealtToChampions'),
                    'magicdamagetaken': stats.get('magicDamageTaken'),
                    'physicaldamagedealt': stats.get('physicalDamageDealt'),
                    'physicaldamagedealttochampions': stats.get('physicalDamageDealtToChampions'),
                    'physicaldamagetaken': stats.get('physicalDamageTaken'),
                    'truedamagedealt': stats.get('trueDamageDealt'),
                    'truedamagedealttochampions': stats.get('trueDamageDealtToChampions'),
                    'truedamagetaken': stats.get('trueDamageTaken'),
                    'totaldamageshieldedonteammates': stats.get('totalDamageShieldedOnTeammates'),
                    
                    # Healing and Survival
                    'totalheal': stats.get('totalHeal'),
                    'totalhealsonteammates': stats.get('totalHealsOnTeammates'),
                    'totaltimespentdead': stats.get('totalTimeSpentDead'),
                    'longesttimespentliving': stats.get('longestTimeSpentLiving'),
                    
                    # Challenges
                    'challenges_kda': stats.get('challenges.kda'),
                    'challenges_damageperminute': stats.get('challenges.damagePerMinute'),
                    'challenges_teamdamagepercentage': stats.get('challenges.teamDamagePercentage'),
                    
                    # Gold and Economy
                    'goldearned': stats.get('goldEarned'),
                    'goldspent': stats.get('goldSpent'),
                    'bountylevel': stats.get('bountyLevel'),
                    'challenges_goldperminute': stats.get('challenges.goldPerMinute'),
                    'challenges_goldshare': stats.get('challenges.goldShare'),
                    
                    # Minions and CS
                    'totalminionskilled': stats.get('totalMinionsKilled'),
                    'neutralminionskilled': stats.get('neutralMinionsKilled'),
                    'totalallyjungleminionskilled': stats.get('totalAllyJungleMinionsKilled'),
                    'totalenemyjungleminionskilled': stats.get('totalEnemyJungleMinionsKilled'),
                    'challenges_csperminute': stats.get('challenges.csPerMinute'),
                    'challenges_maxcsadvantageonlaneopponent': stats.get('challenges.maxCsAdvantageOnLaneOpponent'),
                    'challenges_junglecsbefore10minutes': stats.get('challenges.jungleCsBefore10Minutes'),
                    
                    # Vision
                    'visionscore': stats.get('visionScore'),
                    'wardsplaced': stats.get('wardsPlaced'),
                    'wardskilled': stats.get('wardsKilled'),
                    'visionwardsboughtingame': stats.get('visionWardsBoughtInGame'),
                    'sightwardsboughtingame': stats.get('sightWardsBoughtInGame'),
                    'challenges_visionscoreperminute': stats.get('challenges.visionScorePerMinute'),
                    'challenges_visionscoreadvantagelaneopponent': stats.get('challenges.visionScoreAdvantageLaneOpponent'),
                    'challenges_wardtakedowns': stats.get('challenges.wardTakedowns'),
                    'challenges_wardtakedownsbefore20m': stats.get('challenges.wardTakedownsBefore20M'),
                    'challenges_wardsguarded': stats.get('challenges.wardsGuarded'),
                    'challenges_stealthwardsplaced': stats.get('challenges.stealthWardsPlaced'),
                    
                    # Objectives
                    'turretkills': stats.get('turretKills'),
                    'turrettakedowns': stats.get('turretTakedowns'),
                    'turretslost': stats.get('turretsLost'),
                    'inhibitorkills': stats.get('inhibitorKills'),
                    'inhibitortakedowns': stats.get('inhibitorTakedowns'),
                    'inhibitorslost': stats.get('inhibitorsLost'),
                    'baronkills': stats.get('baronKills'),
                    'dragonkills': stats.get('dragonKills'),
                    'objectivesstolen': stats.get('objectivesStolen'),
                    'objectivesstolenassists': stats.get('objectivesStolenAssists'),
                    'firsttowerkill': stats.get('firstTowerKill'),
                    'firsttowerassist': stats.get('firstTowerAssist'),
                    'challenges_dragontakedowns': stats.get('challenges.dragonTakedowns'),
                    'challenges_elderdragonmultikills': stats.get('challenges.elderDragonMultikills'),
                    'challenges_elderdragonkillswithopposingsoul': stats.get('challenges.elderDragonKillsWithOpposingSoul'),
                    'challenges_teambaronkills': stats.get('challenges.teamBaronKills'),
                    'challenges_teamelderdragonkills': stats.get('challenges.teamElderDragonKills'),
                    'challenges_teamriftheraldkills': stats.get('challenges.teamRiftHeraldKills'),
                    'challenges_riftheraldtakedowns': stats.get('challenges.riftHeraldTakedowns'),
                    'challenges_turretplatestaken': stats.get('challenges.turretPlatesTaken'),
                    'challenges_turretstakenwithriftherald': stats.get('challenges.turretsTakenWithRiftHerald'),
                    'challenges_firstturretkilled': stats.get('challenges.firstTurretKilled'),
                    'challenges_firstturretkilledtime': stats.get('challenges.firstTurretKilledTime'),
                    'challenges_quickfirstturret': stats.get('challenges.quickFirstTurret'),
                    
                    # Pings
                    'onmywaypings': stats.get('onMyWayPings'),
                    'retreatpings': stats.get('retreatPings'),
                    'getbackpings': stats.get('getBackPings'),
                    'dangerpings': stats.get('dangerPings'),
                    'enemymissingpings': stats.get('enemyMissingPings'),
                    'enemyvisionpings': stats.get('enemyVisionPings'),
                    'pushpings': stats.get('pushPings'),
                    'commandpings': stats.get('commandPings'),
                    'needvisionpings': stats.get('needVisionPings'),
                    'visionclearedpings': stats.get('visionClearedPings'),
                    'holdpings': stats.get('holdPings'),
                    
                    # Items
                    'item0': stats.get('item0'),
                    'item1': stats.get('item1'),
                    'item2': stats.get('item2'),
                    'item3': stats.get('item3'),
                    'item4': stats.get('item4'),
                    'item5': stats.get('item5'),
                    'item6': stats.get('item6'),
                    'itemspurchased': stats.get('itemsPurchased'),
                    
                    # More Challenges
                    'challenges_dodgeskillshotssmallwindow': stats.get('challenges.dodgeSkillShotsSmallWindow'),
                    'challenges_skillshotshit': stats.get('challenges.skillshotsHit'),
                    'challenges_tooklargedamagesurvived': stats.get('challenges.tookLargeDamageSurvived'),
                    'challenges_pickkillwithally': stats.get('challenges.pickKillWithAlly'),
                    'challenges_solokills': stats.get('challenges.soloKills'),
                    'challenges_quicksolokills': stats.get('challenges.quickSoloKills'),
                    'challenges_unseenrecalls': stats.get('challenges.unseenRecalls'),
                    'challenges_gamelength': stats.get('challenges.gameLength'),
                    'challenges_outnumberedkills': stats.get('challenges.outnumberedKills'),
                    'challenges_earlylaningphasegoldexpadvantage': stats.get('challenges.earlyLaningPhaseGoldExpAdvantage'),
                    'challenges_effectivehealandshielding': stats.get('challenges.effectiveHealAndShielding'),
                    'challenges_maxlevelleadlaneopponent': stats.get('challenges.maxLevelLeadLaneOpponent'),
                    'challenges_takedowns': stats.get('challenges.takedowns'),
                    'challenges_takedownsaftergainingleveladvantage': stats.get('challenges.takedownsAfterGainingLevelAdvantage'),
                    'challenges_takedownsbeforejungleminionspawn': stats.get('challenges.takedownsBeforeJungleMinionSpawn'),
                    'challenges_hadopennexus': stats.get('challenges.hadOpenNexus'),
                    'challenges_voidmonsterkill': stats.get('challenges.voidMonsterKill'),
                    
                    # Experience and Time
                    'timeplayed': stats.get('timePlayed'),
                    'champexperience': stats.get('champExperience'),
                    'champlevel': stats.get('champLevel'),
                }
                converted_data = {}
                for column_name, value in mapped_data.items():
                    converted_data[column_name] = convert_value_for_db(value, column_name)
                
                # Filter out None values to avoid database errors
                mapped_data = {k: v for k, v in converted_data.items() if v is not None}
                
                # Create the SQL query dynamically based on available keys
                columns = ', '.join(mapped_data.keys())
                placeholders = ', '.join([f'%({key})s' for key in mapped_data.keys()])
                
                cur.execute(f"""
                    INSERT INTO match_stats ({columns})
                    VALUES ({placeholders})
                    ON CONFLICT (match_id, puuid) DO NOTHING
                """, mapped_data)
        
        conn.commit()
        print(f" Successfully saved {len(stats_list)} match stats to database.")
        
    except Exception as e:
        conn.rollback()
        print(f" Error saving match stats: {e}")
        raise
    finally:
        conn.close()


def save_timeline_metrics(metrics_list):
    """
    Takes timeline metrics with camelCase keys and inserts them into match_timelines table.
    """
    if not metrics_list:
        print(" No timeline metrics to save.")
        return

    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            for metrics in metrics_list:
                mapped_data = {
                    'match_id': metrics.get('matchId'),
                    'puuid': metrics.get('puuid'),
                    'match_duration_min': metrics.get('matchDurationMin'),
                    'timeline_data': json.dumps(metrics)   # The entire camelCase dictionary as JSON
                }
                
                # Filter out None values
                mapped_data = {k: v for k, v in mapped_data.items() if v is not None}
                
                cur.execute("""
                    INSERT INTO match_timelines 
                    (match_id, puuid, match_duration_min,  timeline_data)
                    VALUES (%(match_id)s, %(puuid)s, %(match_duration_min)s, 
                             %(timeline_data)s)
                    ON CONFLICT (match_id, puuid) DO NOTHING
                """, mapped_data)
        
        conn.commit()
        print(f" Successfully saved {len(metrics_list)} timeline metrics to database.")
        
    except Exception as e:
        conn.rollback()
        print(f" Error saving timeline metrics: {e}")
        raise
    finally:
        conn.close()


def convert_value_for_db(value, column_name):
    """Convert values to match the database column types."""
    if value is None:
        return None
    
    # Boolean columns
    boolean_columns = [
        'challenges_firstturretkilled',
        'challenges_quickfirstturret', 
        'challenges_hadopennexus',
        'win',
        'firstbloodkill',
        'firstbloodassist',
        'firsttowerkill',
        'firsttowerassist',
        'gameendedinsurrender',
        'gameendedinearlysurrender'
    ]
    
    if column_name in boolean_columns:
        # Convert to boolean: 0/1 -> False/True, "true"/"false" -> True/False
        if isinstance(value, bool):
            return value
        elif isinstance(value, int):
            return bool(value)
        elif isinstance(value, str):
            return value.lower() in ['true', '1', 'yes']
        else:
            return bool(value)
    
    # For other types, let PostgreSQL handle the conversion
    return value