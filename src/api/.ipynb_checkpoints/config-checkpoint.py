import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Riot API Key (Loaded from .env)
RIOT_API_KEY = os.getenv("RIOT_API_KEY")

# Check if the key is loaded correctly
if not RIOT_API_KEY:
    raise ValueError(" ERROR: Riot API Key is missing! Add it to the .env file.")
