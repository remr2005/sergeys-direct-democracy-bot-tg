from pyrogram import Client, filters
from pyrogram.types import Message, ChatPermissions
import vote

def register_removeAdmin_command(app: Client):
    @app.on_message(filters.command("remove_admin"))
    async def removeAdmin(client: Client, message: Message):
        # TODO: сделать удаление админки, а не кослыть с забиранием
        print("removeAdmin command received")
        # Берем параметры функции
        args = message.text.split()[1:]
        # Проверка на правильное написание
        if len(args)==0 or len(args)>1:     
            await message.reply("Ауч, вы написали какую то поеботу. Используйте /help remove_admin, что бы узнать как пользоваться этой функцией")
            return
        #Получаем ID юзера
        user = await client.get_users(args[0][1:])
        if await vote.vote(message,client,f"Забрать ли у юзера {args[0]}, роль админа?",1):
            #выдача админки
            try:
                await client.restrict_chat_member(message.chat.id,
                                                user.id,
                                                permissions=ChatPermissions.default(message.chat)['permissions']
                                                )
                print(f"Права администратора у пользователя {user.id} в чате {message.chat.id} были успешно удалены.")
                await message.reply(f"У юзера {args[0]} отозваны права админа")
            except:
                await message.reply("Произошла ошибка")
        else:
            await message.reply("Голосование провалилось")
