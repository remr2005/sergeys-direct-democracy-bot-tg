from pyrogram import Client, filters

def register_changeName_command(app: Client):
    @app.on_message(filters.command("change_name"))
    async def changeName(client, message):
        print("changeName command received")
        await message.reply('''В общем, здрасте. Список всех доступных команд:
                            make_admin''')
