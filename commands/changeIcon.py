from pyrogram import Client, filters
from pyrogram.types import Message
import vote

def register_changeIcon_command(app: Client):
    @app.on_message(filters.command("change_icon"))
    async def changeIcon(client: Client, message: Message):
        print("changeIcon command received")
        if await vote.vote(message, client, f"Should the group icon be changed to the one suggested above?", 60*60*12):
            if message.photo:
                # Uploading photo
                photo = message.photo  # Get the photo with the highest resolution
                photo_file_path = await client.download_media(photo.file_id)
                
                try:
                    # Setting the new group icon
                    await client.set_chat_photo(chat_id=message.chat.id, photo=photo_file_path)
                    await message.reply_text("The group icon has been successfully changed!")
                except Exception as e:
                    await message.reply_text(f"An error occurred: {e}")
            else:
                await message.reply_text("Please attach a photo to the /setgroupicon command.")
        else:
            await message.reply("The vote failed")
