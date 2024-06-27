from pyrogram import Client, filters
from pyrogram.types import Message

def register_help_command(app: Client):
    @app.on_message(filters.command("help"))
    async def help(client: Client, message: Message):
        print("Help command received")
        args = message.text.split()[1:]
        if len(args)==0:
            await message.reply('''В общем, здрасте. Список всех доступных команд:
                                make_admin
                                remove_admin
                                invite
                                kick
                                change_icon
                                change_name
                                а так же множество других, секретных команд...''')
        if args[0]=="make_admin":
            await message.reply("""Команда /make_admin, создание голосование по поводу выдачи админки.
Использование: /make_admin [user]
Пример: /make_admin @example_user""")
