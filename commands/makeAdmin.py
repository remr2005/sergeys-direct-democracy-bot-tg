from pyrogram import Client, filters
import vote
from pyrogram.types import Message, ChatPrivileges

def register_makeAdmin_command(app: Client):
    @app.on_message(filters.command("make_admin"))
    async def makeAdmin(client: Client, message: Message):
        print("makeAdmin command received")
        # Берем параметры функции
        args = message.text.split()[1:]
        # Проверка на правильное написание TODO сделать более тонкую настройку админа
        if len(args)==0 or len(args)>1:     
            await message.reply("Ауч, вы написали какую то поеботу. Используйте /help make_admin, что бы узнать как пользоваться этой функцией")
            return
        #Получаем ID юзера
        user = await client.get_users(args[0][1:])
        
        if await vote.vote(message,client,f"Дать ли юзеру {args[0]}, роль админа?",60*60*12):
            #выдача админки
            try:
                await client.promote_chat_member(
                    chat_id=message.chat.id,
                    user_id=user.id,
                    privileges=ChatPrivileges(
                        can_delete_messages=True,
                        can_manage_video_chats=True,
                        can_restrict_members=True,
                        can_change_info=True,
                        can_invite_users=True,
                        can_pin_messages=True
                    )
                )
                print(f"Пользователь {user.id} назначен администратором в чате {message.chat.id}")
                await message.reply(f"Юзеру {args[0]} выданы права админа")
            except Exception as e:
                message.reply_text(f"Произошла ошибка: {e}")
        else:
            await message.reply("Голосование провалилось")
