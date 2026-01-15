"""
Remove admin command module for the Telegram bot.

Allows users to vote on removing admin privileges from a group member.
If the vote passes, the user's admin rights are revoked.
"""

import logging

from pyrogram import Client, filters
from pyrogram.types import ChatPermissions, Message

import vote

logger = logging.getLogger(__name__)


def register_removeAdmin_command(app: Client):
    """
    Register remove_admin command handler with the Pyrogram client.

    Registers the /remove_admin command which creates a vote to revoke
    admin privileges from a user.

    Args:
        app: Pyrogram Client instance to register handlers with
    """

    @app.on_message(filters.command("remove_admin"))
    async def removeAdmin(client: Client, message: Message):
        """
        Handle /remove_admin command to vote on removing admin privileges.

        Creates a poll to vote on revoking admin rights from a specified user.
        If the vote passes, the user's admin privileges are removed and
        they receive default chat permissions.

        Usage: /remove_admin @username

        Args:
            client: Pyrogram client instance
            message: The message containing the remove_admin command
        """
        logger.info(f"RemoveAdmin command received from user {message.from_user.id} in chat {message.chat.id}")
        # Get function parameters
        args = message.text.split()[1:]
        # Check for correct usage
        if len(args) == 0 or len(args) > 1:
            logger.warning(f"Invalid remove_admin command usage from user {message.from_user.id}: {message.text}")
            await message.reply(
                "Ouch, you wrote something wrong. Use /help remove_admin to learn how to use this function."
            )
            return
        # Get user ID
        user = await client.get_users(args[0][1:])
        logger.info(f"RemoveAdmin vote initiated for user {user.id} ({args[0]}) in chat {message.chat.id}")
        if await vote.vote(
            message,
            client,
            f"Should admin rights be revoked from {args[0]}?",
            60 * 60 * 12,
        ):
            # Removing admin rights
            try:
                await client.restrict_chat_member(
                    message.chat.id,
                    user.id,
                    permissions=ChatPermissions.default(message.chat)["permissions"],
                )
                logger.info(
                    f"Admin rights were successfully revoked from user {user.id} ({args[0]}) in chat {message.chat.id}"
                )
                await message.reply(f"Admin rights have been revoked from {args[0]}")
            except Exception as e:
                logger.error(f"Failed to revoke admin rights from user {user.id} ({args[0]}) in chat {message.chat.id}: {e}", exc_info=True)
                await message.reply_text(f"An error occurred: {e}")
        else:
            logger.info(f"RemoveAdmin vote failed for user {user.id} ({args[0]}) in chat {message.chat.id}")
            await message.reply("The vote failed")
