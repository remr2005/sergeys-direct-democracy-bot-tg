from pyrogram import Client, filters
import vote
import datetime
from pyrogram.types import Message, ChatPrivileges

users_in_jail = {}
users_in_jail_time = {}

def register_jail_command(app: Client):
    @app.on_message(filters.command("go_to_jail"))
    async def jail(client: Client, message: Message):
        print("jail command received")
        # Берем параметры функции
        args = message.text.split()[1:]
        # Проверка на правильное написание TODO сделать более тонкую настройку админа
        if len(args)==0 or len(args)>1:     
            await message.reply("Ауч, вы написали какую то поеботу. Используйте /help make_admin, что бы узнать как пользоваться этой функцией")
            return
        #Получаем ID юзера
        user = await client.get_users(args[0][1:])
        if await vote.vote(message,client,f"Послать ли юзера {args[0]} в тюрягу?",3):
            # try:
            # if  not(message.chat.id in users_in_jail.keys()):
            #     print(1)
            #     users_in_jail[message.chat.id]=[message.from_user.id]
            # else:
            #     print(2)
            #     users_in_jail[message.chat.id]+=[message.from_user.id]
            users_in_jail_time[(message.chat.id, user.id)] = datetime.datetime.now()+ datetime.timedelta(minutes=15)
            print(users_in_jail_time)
            # print(users_in_jail)
            await message.reply(f"Пользователь {args[0]} пошел в тюрягу")
            # except Exception as e:
            #     await message.reply_text(f"Произошла ошибка: {e}")
        else:
            await message.reply("Голосование провалилось")
            
    @app.on_message()
    async def go_to_jail(client: Client, message: Message):
        try:
            if users_in_jail_time[(message.chat.id, message.from_user.id)]<datetime.datetime.now():
                users_in_jail_time.pop((message.chat.id, message.from_user.id)) 
                print(f"{message.from_user.id} был освобожден в чате {message.chat.id}")
        except Exception as e:
            return

        # if not (message.from_user.id in users_in_jail[message.chat.id]):
        #     returns

        try:
            print(f"{message.from_user.first_name} пытался выбраться из тюряги")
            await client.delete_messages(chat_id=message.chat.id, message_ids=message.id)
        except Exception as e:
            print(f"Failed to delete message {message.id}: {e}")
