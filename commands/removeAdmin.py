from pyrogram import Client, filters
from pyrogram.types import Message, ChatPrivileges
import vote

def register_removeAdmin_command(app: Client):
    @app.on_message(filters.command("remove_admin"))
    async def removeAdmin(client: Client, message: Message):
        # TODO: сделать удаление админки, а не кослыть с забиранием
        print("removeAdmin command received")
        # Берем параметры функции
        args = message.text.split()[1:]
        # Проверка на правильное написание
        if len(args)==0:     
            await message.reply("Ауч, вы написали какую то поеботу. Используйте /help remove_admin, что бы узнать как пользоваться этой функцией")
            return
        #Получаем ID юзера
        user = await client.get_users(args[0][1:])
        
        if await vote.vote(message,client,f"Забрать ли у юзера {args[0]}, роль админа?",5):
            #выдача админки
            try:
                await client.promote_chat_member(
                        chat_id=message.chat.id,
                        user_id=user.id,
                        privileges=ChatPrivileges(
                            can_delete_messages=False,
                            can_manage_video_chats=False,
                            can_restrict_members=False,
                            can_change_info=False,
                            can_invite_users=True,
                            can_pin_messages=False
                        )
                    )
                print(f"Права администратора у пользователя {user.id} в чате {message.chat.id} были успешно удалены.")
                await message.reply(f"У юзера {args[0]} отзваны права админа")
            except:
                await message.reply("Произошла ошибка")
        else:
            await message.reply("Голосование провалилось")

        
        
