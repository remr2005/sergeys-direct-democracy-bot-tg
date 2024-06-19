import os
import importlib
from pyrogram import Client, filters

# Ваши данные для подключения к Telegram API
api_id = 'YOUR_API_ID'
api_hash = 'YOUR_API_HASH'
bot_token = 'YOUR_BOT_TOKEN'

# Создание клиента
app = Client("my_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

# Загрузка команд из папки commands
def load_commands(app):
    commands_dir = 'commands'
    for filename in os.listdir(commands_dir):
        if filename.endswith('.py') and filename != '__init__.py':
            module_name = f'{commands_dir}.{filename[:-3]}'
            module = importlib.import_module(module_name)
            for attribute_name in dir(module):
                attribute = getattr(module, attribute_name)
                if callable(attribute):
                    command_name = filename[:-3]
                    app.add_handler(filters.command(command_name)(attribute))

# Запуск бота и загрузка команд
if __name__ == "__main__":
    load_commands(app)
    app.run()
