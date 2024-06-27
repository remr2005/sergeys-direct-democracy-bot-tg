from pyrogram import Client, filters
import asyncio
from pyrogram.types import Message, ChatPrivileges, Poll
import re

def register_makeAdmin_command(app: Client):
    @app.on_message(filters.command("make_admin"))
    async def makeAdmin(client: Client, message: Message):
        print("Make_admins")
        # Берем параметры функции
        args = message.text.split()[1:]
        # Проверка на правильное написание
        # TODO if len(args)<=7 or len(args)>7: await message.reply("Ауч, вы написали какую то поеботу. Используйте /help make_admin, что бы узнать как пользоваться этой функцией")
        #Получаем ID юзера
        user = await client.get_users(args[0][1:])
        
        poll_message = await client.send_poll(
            chat_id=message.chat.id,
            question=f"Дать ли юзеру {args[0]}, роль админа?",
            options=["Да", "Нет"],
            is_anonymous=False  # Устанавливаем False, если хотите, чтобы голосование было неанонимным
        )
        await asyncio.sleep(30)

        results = {option.text: option.voter_count for option in poll_message.poll.options}
        if results["Да"] >= results["Нет"]:
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
            except:
                await message.reply("Произошла ошибка")
            return
        await message.reply("Голосование провалилось")

        