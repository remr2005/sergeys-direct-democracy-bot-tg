"""
Main entry point for the Telegram direct democracy bot.

This module initializes the Pyrogram client, automatically imports and registers
all command handlers from the commands directory, and starts the bot.
"""

import importlib
import logging
import os

from pyrogram import Client

from config import api_hash, api_id, bot_token

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("pyrogram")
logger.setLevel(logging.INFO)

# Initialize the client
logger.info("Initializing bot client...")
app = Client("my_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)
logger.info("Client initialized successfully")

# Automatic import of all modules from the commands folder and command registration
commands_dir = "commands"
logger.info(f"Loading commands from {commands_dir}...")
for filename in os.listdir(commands_dir):
    if filename.endswith(".py") and filename != "__init__.py":
        module_name = f"{commands_dir}.{filename[:-3]}"
        module = importlib.import_module(module_name)
        register_function = getattr(module, f"register_{filename[:-3]}_command")
        register_function(app)
        logger.info(f"Imported and registered {module_name}")

# Check bot startup
logger.info("Bot is running...")

# Start the bot
if __name__ == "__main__":
    app.run()
