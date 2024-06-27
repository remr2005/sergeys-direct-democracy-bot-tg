from pyrogram import Client, filters

def register_invite_command(app: Client):
    @app.on_message(filters.command("invite"))
    async def invite(client, message):
        print("invite command received")
        await message.reply('''В общем, здрасте. Список всех доступных команд:
                            make_admin''')
