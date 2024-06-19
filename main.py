from pyrogram import Client
from config import api_id, api_hash, bot_token
import os
import importlib
import logging

logger = logging.getLogger('pyrogram')
logger.setLevel(logging.DEBUG)

# Инициализация клиента
app = Client("my_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

# Автоматический импорт всех модулей из папки commands и регистрация команд
commands_dir = 'commands'
for filename in os.listdir(commands_dir):
    if filename.endswith('.py') and filename != '__init__.py':
        module_name = f"{commands_dir}.{filename[:-3]}"
        module = importlib.import_module(module_name)
        register_function = getattr(module, f"register_{filename[:-3]}_command")
        register_function(app)
        print(f"Imported and registered {module_name}")

# Проверка запуска
print("Bot is running...")

# Запуск бота
app.run()
