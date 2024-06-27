from pyrogram import Client, filters

def register_removeAdmin_command(app: Client):
    @app.on_message(filters.command("remove_admin"))
    async def removeAdmin(client, message):
        # TODO: сделать удаление админки
        print("Help command received")
        
