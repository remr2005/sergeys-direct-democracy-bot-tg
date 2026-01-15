import importlib
import logging
import os

from pyrogram import Client

from config import api_hash, api_id, bot_token

# Logging information, quite dry, honestly
logger = logging.getLogger("pyrogram")
logger.setLevel(logging.DEBUG)

# Initialize the client
app = Client("my_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

# Automatic import of all modules from the commands folder and command registration
commands_dir = "commands"
for filename in os.listdir(commands_dir):
    if filename.endswith(".py") and filename != "__init__.py":
        module_name = f"{commands_dir}.{filename[:-3]}"
        module = importlib.import_module(module_name)
        register_function = getattr(module, f"register_{filename[:-3]}_command")
        register_function(app)
        print(f"Imported and registered {module_name}")

# Check bot startup
print("Bot is running...")

# Start the bot
if __name__ == "__main__":
    app.run()
