import os

from dotenv import load_dotenv

load_dotenv()

# Just a configuration, nothing much to say, could potentially be moved to main TODO
api_id = os.getenv("ID")
api_hash = os.getenv("HASH")
bot_token = os.getenv("TOKEN")
