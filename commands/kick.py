from pyrogram import Client, filters

def register_kick_command(app: Client):
    @app.on_message(filters.command("kick"))
    async def kick(client, message):
        # TODO: сделать кик 
        print("kick command received")
        
