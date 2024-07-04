from pyrogram import Client, filters
from pyrogram.types import Message, ChatPermissions
import vote

def register_removeAdmin_command(app: Client):
    @app.on_message(filters.command("remove_admin"))
    async def removeAdmin(client: Client, message: Message):
        print("removeAdmin command received")
        # Get function parameters
        args = message.text.split()[1:]
        # Check for correct usage
        if len(args) == 0 or len(args) > 1:     
            await message.reply("Ouch, you wrote something wrong. Use /help remove_admin to learn how to use this function.")
            return
        # Get user ID
        user = await client.get_users(args[0][1:])
        if await vote.vote(message, client, f"Should admin rights be revoked from {args[0]}?", 60*60*12):
            # Removing admin rights
            try:
                await client.restrict_chat_member(
                    message.chat.id,
                    user.id,
                    permissions=ChatPermissions.default(message.chat)['permissions']
                )
                print(f"Admin rights were successfully revoked from user {user.id} in chat {message.chat.id}.")
                await message.reply(f"Admin rights have been revoked from {args[0]}")
            except Exception as e:
                await message.reply_text(f"An error occurred: {e}")
        else:
            await message.reply("The vote failed")
