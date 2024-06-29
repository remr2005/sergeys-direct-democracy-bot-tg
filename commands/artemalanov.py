from pyrogram import Client, filters
from pyrogram.types import Message
import asyncio

def register_artemalanov_command(app: Client):
    @app.on_message(filters.command("артем_аланов_реален"))
    @app.on_message(filters.command("is_artem_alanov_real"))
    async def artemalanov(client: Client, message: Message):
        print("secret command received")
        # Берем параметры функции
        await message.reply("Я не знаю бро")
        await asyncio.sleep(1)
        await message.reply("Но...")
        await asyncio.sleep(2)
        await message.reply("Он уже за твоей спиной")
        await client.send_animation(message.chat.id,"gifs/aalanov.mp4",unsave=True)
