"""
Change name command module for the Telegram bot.

Allows users to vote on changing the group name.
If the vote passes, the group name is updated to the specified name.
"""

import logging

from pyrogram import Client, filters
from pyrogram.types import Message

import vote

logger = logging.getLogger(__name__)


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
        logger.info(f"ChangeName command received from user {message.from_user.id} in chat {message.chat.id}")
        # Get arguments
        args = message.text.split()[1:]
        # Check for correct usage
        if len(args) == 0 or len(args) > 1:
            logger.warning(f"Invalid change_name command usage from user {message.from_user.id}: {message.text}")
            await message.reply(
                "Ouch, you wrote something wrong. Use /help change_name to learn how to use this function."
            )
            return
        logger.info(f"ChangeName vote initiated: '{args[0]}' for chat {message.chat.id}")
        # Voting and decision making
        if await vote.vote(
            message,
            client,
            f"Should the group name be changed to {args[0]}",
            60 * 60 * 12,
        ):
            try:
                await client.set_chat_title(message.chat.id, args[0])
                logger.info(f"Group name changed to '{args[0]}' in chat {message.chat.id}")
            except Exception as e:
                logger.error(f"Failed to change chat title to '{args[0]}' in chat {message.chat.id}: {e}", exc_info=True)
                await message.reply_text(f"An error occurred: {e}")
        else:
            logger.info(f"ChangeName vote failed for chat {message.chat.id}")
            await message.reply("The vote failed")
