"""
Kick command module for the Telegram bot.

Allows users to vote on kicking a member from the group.
If the vote passes, the user is temporarily banned for 1 minute.
"""

import logging
from datetime import datetime, timedelta

from pyrogram import Client, filters
from pyrogram.types import Message

import vote

logger = logging.getLogger(__name__)


def register_kick_command(app: Client):
    """
    Register kick command handler with the Pyrogram client.

    Registers the /kick command which creates a vote to kick a user.
    If the vote passes, the user is banned for 1 minute.

    Args:
        app: Pyrogram Client instance to register handlers with
    """

    @app.on_message(filters.command("kick"))
    async def kick(client: Client, message: Message):
        """
        Handle /kick command to vote on kicking a user.

        Creates a poll to vote on kicking a specified user.
        If the vote passes, the user is temporarily banned for 1 minute.

        Usage: /kick @username

        Args:
            client: Pyrogram client instance
            message: The message containing the kick command
        """
        logger.info(f"Kick command received from user {message.from_user.id} in chat {message.chat.id}")
        # Get function parameters
        args = message.text.split()[1:]
        # Check for correct usage TODO make more fine-tuned admin settings
        if len(args) == 0 or len(args) > 1:
            logger.warning(f"Invalid kick command usage from user {message.from_user.id}: {message.text}")
            await message.reply(
                "Ouch, you wrote something wrong. Use /help kick to learn how to use this function."
            )
            return
        # Get user ID
        user = await client.get_users(args[0][1:])
        logger.info(f"Kick vote initiated for user {user.id} ({args[0]}) in chat {message.chat.id}")
        if await vote.vote(
            message, client, f"Should the user {args[0]} be kicked?", 60 * 60 * 12
        ):
            # Kick
            try:
                # Time until the user will be banned (e.g., for 1 minute)
                await app.ban_chat_member(
                    message.chat.id, user.id, datetime.now() + timedelta(minutes=1)
                )
                logger.info(f"User {user.id} ({args[0]}) has been kicked from chat {message.chat.id}")
                await message.reply(f"The user {args[0]} has been kicked")
            except Exception as e:
                logger.error(f"Failed to kick user {user.id} ({args[0]}) from chat {message.chat.id}: {e}", exc_info=True)
                await message.reply_text(f"An error occurred: {e}")
        else:
            logger.info(f"Kick vote failed for user {user.id} ({args[0]}) in chat {message.chat.id}")
            await message.reply("The vote failed")
