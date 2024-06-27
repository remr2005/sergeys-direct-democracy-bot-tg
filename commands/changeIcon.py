from pyrogram import Client, filters

def register_changeIcon_command(app: Client):
    @app.on_message(filters.command("change_icon"))
    async def changeIcon(client, message):
        print("changeIcon command received")
        await message.reply('''В общем, здрасте. Список всех доступных команд:
                            make_admin''')
