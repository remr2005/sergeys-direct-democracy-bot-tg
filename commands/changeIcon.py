"""
Change icon command module for the Telegram bot.

Allows users to vote on changing the group icon.
If the vote passes, the group icon is changed to the photo attached to the command.
"""

from pyrogram import Client, filters
from pyrogram.types import Message

import vote


def register_changeIcon_command(app: Client):
    """
    Register change_icon command handler with the Pyrogram client.

    Registers the /change_icon command which creates a vote to change
    the group icon to an attached photo.

    Args:
        app: Pyrogram Client instance to register handlers with
    """

    @app.on_message(filters.command("change_icon"))
    async def changeIcon(client: Client, message: Message):
        """
        Handle /change_icon command to vote on changing group icon.

        Creates a poll to vote on changing the group icon to the photo
        attached to the command message. If the vote passes, the group
        icon is updated.

        Usage: /change_icon (with a photo attached)

        Args:
            client: Pyrogram client instance
            message: The message containing the change_icon command and photo
        """
        print("changeIcon command received")
        if await vote.vote(
            message,
            client,
            "Should the group icon be changed to the one suggested above?",
            60 * 60 * 12,
        ):
            if message.photo:
                # Uploading photo
                photo = message.photo  # Get the photo with the highest resolution
                photo_file_path = await client.download_media(photo.file_id)

                try:
                    # Setting the new group icon
                    await client.set_chat_photo(
                        chat_id=message.chat.id, photo=photo_file_path
                    )
                    await message.reply_text(
                        "The group icon has been successfully changed!"
                    )
                except Exception as e:
                    await message.reply_text(f"An error occurred: {e}")
            else:
                await message.reply_text(
                    "Please attach a photo to the /setgroupicon command."
                )
        else:
            await message.reply("The vote failed")
