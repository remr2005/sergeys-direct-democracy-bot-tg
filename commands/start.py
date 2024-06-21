from pyrogram import Client, filters

def register_start_command(app: Client):
    @app.on_message(filters.command("start"))  
    async def start(client, message):
    	print("Start command received")  
        await message.reply("Hello! I'm your bot.")  
