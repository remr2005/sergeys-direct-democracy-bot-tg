from pyrogram import Client, filters
from pyrogram.types import Message
import asyncio

def register_secret_command(app: Client):
    @app.on_message(filters.command("секрет"))
    @app.on_message(filters.command("secret"))
    async def secret(client: Client, message: Message):
        # Just a secret function
        print("secret command received")
        await message.reply("VVEEERRRYY SECRRRETTT MESSAGE, CHERESH")
        await message.reply("3")
        await asyncio.sleep(1)
        await message.reply("2")
        await asyncio.sleep(1)
        await message.reply("1")
        await client.send_animation(message.chat.id, "gifs/secret.mp4", unsave=True)
