from pyrogram import Client, filters

def register_help_command(app: Client):
    @app.on_message(filters.command("help"))
    async def help(client, message):
        print("Help command received")
        await message.reply('''В общем, здрасте. Список всех доступных команд:
                            make_admin
                            remove_admin
                            invite
                            kick
                            change_icon
                            change_name''')
