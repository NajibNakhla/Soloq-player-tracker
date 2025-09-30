import unittest
from src.api.get_puuid import get_puuid
from src.api.get_match_history import get_match_history
from src.api.get_match_details import get_match_details
from src.processing.process_multiple_matches import process_multiple_matches

class TestProcessing(unittest.TestCase):

    def setUp(self):
        self.region = "europe"
        self.game_name = "Nakla"
        self.tag_line = "EUW"
        self.target_puuid = "pDeG-TQhQ1svoperQikw5W_2V_wjUrbeasNksOAME_HRqQ2sbPwx4zTg72nS8JZKqUOKAYFBS85J-A"

    def test_process_single_match(self):
        """Test processing a single match"""
        # Get real match data
        match_ids, _ = get_match_history(self.region, self.target_puuid, max_matches=1)
        match_data, _ = get_match_details(self.region, match_ids[0])
        
        # Process it
        result = process_multiple_matches([match_data], self.target_puuid)
        
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 1)
        self.assertIn('matchId', result[0])
        self.assertIn('puuid', result[0])
        self.assertIn('championName', result[0])
        
        print(f" Processed match: {result[0]['matchId']} as {result[0]['championName']} on side : {result[0]['side']}  ,,{result[0]['teamId']} ")

if __name__ == "__main__":
    unittest.main()