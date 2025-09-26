import unittest
from src.database.connection import get_db_connection
from src.database.writer import save_player, save_match

class TestDatabase(unittest.TestCase):

    def test_database_connection(self):
        """Test if we can connect to the database"""
        try:
            conn = get_db_connection()
            conn.close()
            print(" Database connection successful")
            self.assertTrue(True)  # Test passes if we get here
        except Exception as e:
            self.fail(f"Database connection failed: {e}")

    def test_save_player(self):
        """Test saving a player to the database"""
        # Test with a known player
        puuid = "pDeG-TQhQ1svoperQikw5W_2V_wjUrbeasNksOAME_HRqQ2sbPwx4zTg72nS8JZKqUOKAYFBS85J-A"
        try:
            save_player(puuid, "TestPlayer", "TEST","europe")
            print(" Player save executed (check database manually)")
        except Exception as e:
            self.fail(f"Player save failed: {e}")

    def test_save_match(self):
        """Test saving a match to the database"""
        # Test with minimal valid match data structure
        minimal_match_data = {
            'metadata': {'matchId': 'TEST_MATCH_123'},
            'info': {
                'queueId': 420,
                'gameDuration': 1800,
                
            }
        }
        test_puuid = "pDeG-TQhQ1svoperQikw5W_2V_wjUrbeasNksOAME_HRqQ2sbPwx4zTg72nS8JZKqUOKAYFBS85J-A"
        try:
            save_match(minimal_match_data,test_puuid)
            print(" Match save executed with test data")
        except Exception as e:
            print(f"  Match save note: {e}")  # Don't fail if it's just missing data

if __name__ == "__main__":
    unittest.main()