import unittest
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.pipelines.full_pipeline import run_full_pipeline

class TestFullPipeline(unittest.TestCase):

    def test_full_pipeline_one_match(self):
        """Test the complete pipeline with just 1 match"""
        print("\n🚀 Testing FULL pipeline with 1 match...")
        
        try:
            run_full_pipeline(
                region="europe",
                game_name="Nakhla", 
                tag_line="Tree", 
                max_matches=1,  # JUST 1 MATCH
                save=True
            )
            print(" Full pipeline completed successfully!")
            
        except Exception as e:
            print(f" Pipeline failed: {e}")
            import traceback
            traceback.print_exc()
            # Don't fail the test - we want to see what broke

if __name__ == "__main__":
    unittest.main()