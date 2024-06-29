from pyrogram import Client, filters
from pyrogram.types import Message
import json
import vote

def register_invite_command(app: Client):
    @app.on_message(filters.command("invite"))
    async def invite(client: Client, message: Message):
        print("invite command received")
        # Берем параметры функции
        args = message.text.split()[1:]
        # Проверка на правильное написание TODO сделать более тонкую настройку админа
        if len(args)>0:     
            await message.reply("Ауч, вы написали какую то поеботу. Используйте /help invite, что бы узнать как пользоваться этой функцией")
            return
       
        if await vote.vote(message,client,f"Дать ли ссылку инвайт {message.from_user.first_name}?",60*60*12):
            # добавление
            try:
            # Время, до которого пользователь будет забанен (например, на 1 день)
                link_json = await client.create_chat_invite_link(message.chat.id)
                link = dict(json.loads(str(link_json)))["invite_link"]
                await message.reply(f"Юзеру {message.from_user.first_name} отправлено приглашение")
                await client.send_message(
                    chat_id=message.from_user.id,
                    text=f"Пиздуй сюда чепух --> {link}")
            except Exception as e:
                message.reply_text(f"Произошла ошибка: {e}")
        else:
            await message.reply("Голосование провалилось")

