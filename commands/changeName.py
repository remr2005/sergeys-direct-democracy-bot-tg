from pyrogram import Client, filters
from pyrogram.types import Message
import vote

def register_changeName_command(app: Client):
    @app.on_message(filters.command("change_name"))
    async def changeName(client: Client, message: Message):
        print("changeName command received")
        # Get arguments
        args = message.text.split()[1:]
        # Check for correct usage
        if len(args) == 0 or len(args) > 1:     
            await message.reply("Ouch, you wrote something wrong. Use /help change_name to learn how to use this function.")
            return
        # Voting and decision making
        if await vote.vote(message, client, f"Should the group name be changed to {args[0]}", 60*60*12):   
            try:
                await client.set_chat_title(message.chat.id, args[0])
            except Exception as e:
                await message.reply_text(f"An error occurred: {e}")
        else:
            await message.reply("The vote failed")
