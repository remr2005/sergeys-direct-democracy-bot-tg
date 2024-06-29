from pyrogram import Client, filters
from pyrogram.types import Message

def register_maslenko_command(app: Client):
    @app.on_message(filters.command("антон_масленок_реален"))
    @app.on_message(filters.command("is_anton_maslenko_real"))
    async def maslenko(client: Client, message: Message):
        print("secret command received")
        # Берем параметры функции
        await message.reply("Он уже едет, погоди немного")
        await client.send_animation(message.chat.id,"gifs/maslenko.mp4",unsave=True)
