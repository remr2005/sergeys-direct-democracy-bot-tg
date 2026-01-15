"""
Change name command module for the Telegram bot.

Allows users to vote on changing the group name.
If the vote passes, the group name is updated to the specified name.
"""

from pyrogram import Client, filters
from pyrogram.types import Message

import vote


def register_changeName_command(app: Client):
    """
    Register change_name command handler with the Pyrogram client.

    Registers the /change_name command which creates a vote to change
    the group name.

    Args:
        app: Pyrogram Client instance to register handlers with
    """

    @app.on_message(filters.command("change_name"))
    async def changeName(client: Client, message: Message):
        """
        Handle /change_name command to vote on changing group name.

        Creates a poll to vote on changing the group name to a specified name.
        If the vote passes, the group name is updated.

        Usage: /change_name new_group_name

        Args:
            client: Pyrogram client instance
            message: The message containing the change_name command and new name
        """
        print("changeName command received")
        # Get arguments
        args = message.text.split()[1:]
        # Check for correct usage
        if len(args) == 0 or len(args) > 1:
            await message.reply(
                "Ouch, you wrote something wrong. Use /help change_name to learn how to use this function."
            )
            return
        # Voting and decision making
        if await vote.vote(
            message,
            client,
            f"Should the group name be changed to {args[0]}",
            60 * 60 * 12,
        ):
            try:
                await client.set_chat_title(message.chat.id, args[0])
            except Exception as e:
                await message.reply_text(f"An error occurred: {e}")
        else:
            await message.reply("The vote failed")
