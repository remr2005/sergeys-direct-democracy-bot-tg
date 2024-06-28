from pyrogram import Client, filters
import vote
from datetime import datetime, timedelta
from pyrogram.types import Message

def register_kick_command(app: Client):
    @app.on_message(filters.command("kick"))
    async def kick(client:Client, message:Message):
        print("kick command received")
        # Берем параметры функции
        args = message.text.split()[1:]
        # Проверка на правильное написание TODO сделать более тонкую настройку админа
        if len(args)==0 or len(args)>1:     
            await message.reply("Ауч, вы написали какую то поеботу. Используйте /help kick, что бы узнать как пользоваться этой функцией")
            return
        #Получаем ID юзера
        user = await client.get_users(args[0][1:])
        if await vote.vote(message,client,f"Кикнуть ли юзера {args[0]}?",30):
            # кик
            try:
            # Время, до которого пользователь будет забанен (например, на 1 день)
                await app.ban_chat_member(message.chat.id, user.id, datetime.now() + timedelta(minutes=1))
                await message.reply(f"Юзер {args[0]} ликвидирован")
            except Exception as e:
                message.reply_text(f"Произошла ошибка: {e}")
        else:
            await message.reply("Голосование провалилось")

