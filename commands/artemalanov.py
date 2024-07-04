from pyrogram import Client, filters
from pyrogram.types import Message
import asyncio

def register_artemalanov_command(app: Client):
    @app.on_message(filters.command("артем_аланов_реален"))
    @app.on_message(filters.command("is_artem_alanov_real"))
    async def artemalanov(client: Client, message: Message):
        print("secret command received")
        # Just a secret function
        await message.reply("I don't know bro")
        await asyncio.sleep(1)
        await message.reply("But...")
        await asyncio.sleep(2)
        await message.reply("He is already behind you")
        await client.send_animation(message.chat.id,"gifs/aalanov.mp4",unsave=True)
