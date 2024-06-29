from pyrogram import Client, filters
from pyrogram.types import Message
import vote

def register_changeIcon_command(app: Client):
    @app.on_message(filters.command("change_icon"))
    async def changeIcon(client: Client, message: Message):
        print("changeIcon command received")
        # Берем параметры функции
        # Проверка на правильное написание TODO сделать более тонкую настройку админа

        if await vote.vote(message,client,f"Изменить ли аву группы, на то что было предложенно выше?",60*60*12):
            if message.photo:
        # Загрузка фотографии
                photo = message.photo  # Берем фотографию с наибольшим разрешением
                photo_file_path = await client.download_media(photo.file_id)
                
                try:
                    # Установка новой иконки группы
                    await client.set_chat_photo(chat_id=message.chat.id, photo=photo_file_path)
                    await message.reply_text("Иконка группы успешно изменена!")
                except Exception as e:
                    await message.reply_text(f"Произошла ошибка: {e}")
            else:
                await message.reply_text("Пожалуйста, прикрепите фотографию к команде /setgroupicon.")
        else:
            await message.reply("Голосование провалилось")


        
