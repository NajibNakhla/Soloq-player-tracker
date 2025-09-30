import streamlit as st
from src.data.manager import ensure_player_data

def main():
    st.title("📥 Get Player Data")
    st.write("First, let's collect your match data from Riot API.")
    
    game_name = st.text_input("Game Name", placeholder="Nakla")
    tag_line = st.text_input("Tag Line", placeholder="EUW")
    region = st.selectbox("Region", ["europe", "americas", "asia"])
    max_matches = st.slider("Matches to fetch", 10, 500, 100)
    
    if st.button("Collect Data") and game_name and tag_line:
        with st.spinner(f"Fetching {max_matches} matches from Riot API..."):
            try:
                ensure_player_data(region, game_name, tag_line, max_matches)
                
                # ✅ STEP 1: STORE PLAYER IN SESSION STATE
                st.session_state.current_player = {
                    'game_name': game_name,
                    'tag_line': tag_line,
                    'region': region
                }
                
                st.success("✅ Data collection complete!")
                st.balloons()
                
                # Show navigation instructions
                st.info("🎯 You can now navigate to analysis pages to view your stats!")
                
                # Quick preview
                from src.database.connection import get_db_connection
                conn = get_db_connection()
                with conn.cursor() as cur:
                    cur.execute("""
                        SELECT COUNT(*) as match_count 
                        FROM match_stats 
                        WHERE puuid IN (
                            SELECT puuid FROM players 
                            WHERE game_name = %s AND tag_line = %s
                        )
                    """, (game_name, tag_line))
                    count = cur.fetchone()[0]
                    st.info(f"📊 You now have {count} matches in the database!")
                    
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    main()