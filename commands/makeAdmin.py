from pyrogram import Client, filters
from pyrogram.types import ChatPrivileges, Message

import vote


def register_makeAdmin_command(app: Client):
    @app.on_message(filters.command("make_admin"))
    async def makeAdmin(client: Client, message: Message):
        print("makeAdmin command received")
        # Get function parameters
        args = message.text.split()[1:]
        # Check for correct usage TODO make more fine-tuned admin settings
        if len(args) == 0 or len(args) > 1:
            await message.reply(
                "Ouch, you wrote something wrong. Use /help make_admin to learn how to use this function."
            )
            return
        # Get user ID
        user = await client.get_users(args[0][1:])

        if await vote.vote(
            message,
            client,
            f"Should the user {args[0]} be given admin privileges?",
            60 * 60 * 12,
        ):
            # Grant admin privileges
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
                        can_pin_messages=True,
                    ),
                )
                print(
                    f"The user {user.id} has been promoted to admin in chat {message.chat.id}"
                )
                await message.reply(
                    f"The user {args[0]} has been given admin privileges"
                )
            except Exception as e:
                await message.reply_text(f"An error occurred: {e}")
        else:
            await message.reply("The vote failed")
