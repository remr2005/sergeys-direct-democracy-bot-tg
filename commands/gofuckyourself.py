from pyrogram import Client, filters
from pyrogram.types import Message

def register_gofuckyourself_command(app: Client):
    @app.on_message(filters.command("обосрать_штаны"))
    @app.on_message(filters.command("gofuckyourself"))
    async def gofuckyourself(client: Client, message: Message):
        print("secret command received")
        # secret command
        await message.reply("okay")
        await client.send_animation(message.chat.id, "gifs/okay.mp4", unsave=True)
