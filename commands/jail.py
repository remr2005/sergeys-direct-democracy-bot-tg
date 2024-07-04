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
        # Get function parameters
        args = message.text.split()[1:]
        # Check for correct usage TODO make more fine-tuned admin settings
        if len(args) == 0 or len(args) > 1:     
            await message.reply("Ouch, you wrote something wrong. Use /help go_to_jail to learn how to use this function.")
            return
        # Get user ID
        user = await client.get_users(args[0][1:])
        if await vote.vote(message, client, f"Should the user {args[0]} be sent to jail?", 3):
            users_in_jail_time[(message.chat.id, user.id)] = datetime.datetime.now() + datetime.timedelta(minutes=15)
            print(users_in_jail_time)
            await message.reply(f"The user {args[0]} has been sent to jail.")
        else:
            await message.reply("The vote failed")
            
    @app.on_message()
    async def go_to_jail(client: Client, message: Message):
        try:
            if users_in_jail_time[(message.chat.id, message.from_user.id)] < datetime.datetime.now():
                users_in_jail_time.pop((message.chat.id, message.from_user.id)) 
                print(f"{message.from_user.id} has been released in chat {message.chat.id}")
        except Exception as e:
            return
        try:
            print(f"{message.from_user.first_name} tried to escape from jail")
            await client.delete_messages(chat_id=message.chat.id, message_ids=message.id)
        except Exception as e:
            print(f"Failed to delete message {message.id}: {e}")
