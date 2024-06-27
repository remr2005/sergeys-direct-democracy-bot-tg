from pyrogram import Client, filters
from pyrogram.types import Message, ChatPrivileges
import re

def register_makeAdmin_command(app: Client):
    @app.on_message(filters.command("make_admin"))
    async def makeAdmin(client: Client, message: Message):
        print("Make_admins")
        args = message.text.split()[1:]
        user = await client.get_users(args[0][1:])

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

        