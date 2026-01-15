"""
Make admin command module for the Telegram bot.

Allows users to vote on granting admin privileges to a group member.
If the vote passes, the user receives full admin permissions.
"""

import logging

from pyrogram import Client, filters
from pyrogram.types import ChatPrivileges, Message

import vote

logger = logging.getLogger(__name__)


def register_makeAdmin_command(app: Client):
    """
    Register make_admin command handler with the Pyrogram client.

    Registers the /make_admin command which creates a vote to grant
    admin privileges to a user.

    Args:
        app: Pyrogram Client instance to register handlers with
    """

    @app.on_message(filters.command("make_admin"))
    async def makeAdmin(client: Client, message: Message):
        """
        Handle /make_admin command to vote on granting admin privileges.

        Creates a poll to vote on making a specified user an admin.
        If the vote passes, the user receives full admin privileges including:
        - Delete messages
        - Manage video chats
        - Restrict members
        - Change info
        - Invite users
        - Pin messages

        Usage: /make_admin @username

        Args:
            client: Pyrogram client instance
            message: The message containing the make_admin command
        """
        logger.info(f"MakeAdmin command received from user {message.from_user.id} in chat {message.chat.id}")
        # Get function parameters
        args = message.text.split()[1:]
        # Check for correct usage TODO make more fine-tuned admin settings
        if len(args) == 0 or len(args) > 1:
            logger.warning(f"Invalid make_admin command usage from user {message.from_user.id}: {message.text}")
            await message.reply(
                "Ouch, you wrote something wrong. Use /help make_admin to learn how to use this function."
            )
            return
        # Get user ID
        user = await client.get_users(args[0][1:])
        logger.info(f"MakeAdmin vote initiated for user {user.id} ({args[0]}) in chat {message.chat.id}")

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
                logger.info(
                    f"User {user.id} ({args[0]}) has been promoted to admin in chat {message.chat.id}"
                )
                await message.reply(
                    f"The user {args[0]} has been given admin privileges"
                )
            except Exception as e:
                logger.error(f"Failed to promote user {user.id} ({args[0]}) to admin in chat {message.chat.id}: {e}", exc_info=True)
                await message.reply_text(f"An error occurred: {e}")
        else:
            logger.info(f"MakeAdmin vote failed for user {user.id} ({args[0]}) in chat {message.chat.id}")
            await message.reply("The vote failed")
