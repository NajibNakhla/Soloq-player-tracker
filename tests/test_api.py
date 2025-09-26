import unittest
from src.api.get_puuid import get_puuid
from src.api.get_match_history import get_match_history
from src.api.get_match_details import get_match_details
from src.api.get_match_timeline import get_match_timeline
from src.utils.rate_tracker import init_rate_tracker, get_rate_limit_info
import streamlit as st

class TestRiotAPI(unittest.TestCase):

    def setUp(self):
        """Set up test variables and initialize rate tracker"""
        self.region = "europe"
        self.game_name = "Nakhla"  # Fixed typo from "Nakhla" to match your actual test
        self.tag_line = "Tree"     # Fixed from "tree" to actual tag
        init_rate_tracker()  # Initialize rate tracking

    def test_get_puuid(self):
        """Test if we can fetch a valid PUUID and rate info"""
        puuid, rate_info = get_puuid(self.region, self.game_name, self.tag_line)
        
        # Test data
        self.assertIsInstance(puuid, str)
        self.assertGreater(len(puuid), 10)  # PUUID should be reasonably long
        
        # Test rate info
        self.assertIsInstance(rate_info, dict)
        self.assertIn('used', rate_info)
        self.assertIn('max', rate_info)
        self.assertLessEqual(rate_info['used'], rate_info['max'])
        
        print(f" PUUID: {puuid}")
        print(f" Rate Info: {rate_info['used']}/{rate_info['max']}")

    def test_get_match_history(self):
        """Test if we can fetch match IDs with rate info"""
        puuid, _ = get_puuid(self.region, self.game_name, self.tag_line)
        match_ids, rate_info = get_match_history(self.region, puuid, max_matches=1)
        
        # Test data
        self.assertIsInstance(match_ids, list)
        if match_ids:  # If we got matches
            self.assertIsInstance(match_ids[0], str)
            self.assertTrue(match_ids[0].startswith(('EUW1_', 'EUN1_')))  # Match ID format
        
        # Test rate info
        self.assertIsInstance(rate_info, dict)
        self.assertIn('used', rate_info)
        
        print(f" Match IDs: {match_ids}")
        print(f" Rate Info: {rate_info['used']}/{rate_info['max']}")

    def test_get_match_details(self):
        """Test if we can fetch match details with rate info"""
        puuid, _ = get_puuid(self.region, self.game_name, self.tag_line)
        match_ids, _ = get_match_history(self.region, puuid, max_matches=1)
        
        if not match_ids:
            self.skipTest("No match IDs found to test details")
            
        match_data, rate_info = get_match_details(self.region, match_ids[0])
        
        # Test data
        self.assertIsInstance(match_data, dict)
        self.assertIn('metadata', match_data)
        self.assertIn('info', match_data)
        self.assertEqual(match_data['metadata']['matchId'], match_ids[0])
        
        # Test rate info
        self.assertIsInstance(rate_info, dict)
        self.assertIn('used', rate_info)
        
        print(f" Match Data: {match_data['metadata']['matchId']}")
        print(f" Rate Info: {rate_info['used']}/{rate_info['max']}")

    def test_get_match_timeline(self):
        """Test if we can fetch match timeline data with rate info"""
        puuid, _ = get_puuid(self.region, self.game_name, self.tag_line)
        match_ids, _ = get_match_history(self.region, puuid, max_matches=1)
        
        if not match_ids:
            self.skipTest("No match IDs found to test timeline")
            
        timeline_data, rate_info = get_match_timeline(self.region, match_ids[0])
        
        # Test data
        self.assertIsInstance(timeline_data, dict)
        self.assertIn('metadata', timeline_data)
        self.assertIn('info', timeline_data)
        self.assertIn('frames', timeline_data.get('info', {}))
        self.assertGreater(len(timeline_data.get('info', {}).get('frames', [])), 0)
        
        # Test rate info
        self.assertIsInstance(rate_info, dict)
        self.assertIn('used', rate_info)
        
        print(f" Timeline Frames: {len(timeline_data['info']['frames'])}")
        print(f" Rate Info: {rate_info['used']}/{rate_info['max']}")

    def test_rate_tracker_updated(self):
        """Test that the rate tracker is being updated by API calls"""
        # Get initial state
        initial_rate = get_rate_limit_info('account')
        
        # Make API call that should update the tracker
        puuid, rate_info = get_puuid(self.region, self.game_name, self.tag_line)
        
        # Check if tracker was updated
        updated_rate = get_rate_limit_info('account')
        
        # The tracker should reflect the rate info from the API response
        self.assertEqual(updated_rate['used'], rate_info['used'])
        self.assertEqual(updated_rate['max'], rate_info['max'])
        print(f" Rate tracker updated: {updated_rate['used']}/{updated_rate['max']}")

if __name__ == "__main__":
    unittest.main(verbosity=2)  # More detailed output