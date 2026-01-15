"""
Configuration module for the Telegram bot.

Loads environment variables from .env file and provides API credentials
for Pyrogram client initialization.
"""

import os

from dotenv import load_dotenv

load_dotenv()

# Just a configuration, nothing much to say, could potentially be moved to main TODO
api_id = os.getenv("ID")
"""Telegram API ID from environment variables."""

api_hash = os.getenv("HASH")
"""Telegram API hash from environment variables."""

bot_token = os.getenv("TOKEN")
"""Telegram bot token from environment variables."""
