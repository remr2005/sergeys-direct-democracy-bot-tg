from pyrogram import Client, filters
from pyrogram.types import Message
import vote

def register_changeName_command(app: Client):
    @app.on_message(filters.command("change_name"))
    async def changeName(client: Client, message: Message):
        print("changeName command received")
        # берем аргументы
        args = message.text.split()[1:]
        # Проверка на правильное написание
        if len(args)==0 or len(args)>1:     
            await message.reply("Ауч, вы написали какую то поеботу. Используйте /help change_name, что бы узнать как пользоваться этой функцией")
            return
        # голосование и принятие решения
        if await vote.vote(message,client,f"Изменить ли название группы на {args[0]}",60*60*12):   
            try:
                await client.set_chat_title(message.chat.id,args[0])
            except Exception as e:
                await message.reply_text(f"Произошла ошибка: {e}")
        else:
            await message.reply("Голосование провалилось")

