"""
Jail command module for the Telegram bot.

Allows users to vote on sending a user to "jail" for 15 minutes.
Users in jail have their messages automatically deleted until their sentence ends.
"""

import datetime
import logging

from pyrogram import Client, filters
from pyrogram.types import Message

import vote

logger = logging.getLogger(__name__)

users_in_jail = {}
"""Dictionary tracking users currently in jail."""

users_in_jail_time = {}
"""Dictionary tracking when users will be released from jail."""


def register_jail_command(app: Client):
    """
    Register jail command handlers with the Pyrogram client.

    Registers two handlers:
    - /go_to_jail: Creates a vote to send a user to jail
    - Message handler: Deletes messages from users in jail

    Args:
        app: Pyrogram Client instance to register handlers with
    """

    @app.on_message(filters.command("go_to_jail"))
    async def jail(client: Client, message: Message):
        """
        Handle /go_to_jail command to vote on sending a user to jail.

        Creates a poll to vote on sending a specified user to jail for 15 minutes.
        If the vote passes, the user is added to the jail system and their
        messages will be automatically deleted until the sentence ends.

        Usage: /go_to_jail @username

        Args:
            client: Pyrogram client instance
            message: The message containing the go_to_jail command
        """
        logger.info(
            f"Jail command received from user {message.from_user.id} in chat {message.chat.id}"
        )
        # Get function parameters
        args = message.text.split()[1:]
        # Check for correct usage TODO make more fine-tuned admin settings
        if len(args) == 0 or len(args) > 1:
            logger.warning(
                f"Invalid go_to_jail command usage from user {message.from_user.id}: {message.text}"
            )
            await message.reply(
                "Ouch, you wrote something wrong. Use /help go_to_jail to learn how to use this function."
            )
            return
        # Get user ID
        user = await client.get_users(args[0][1:])
        logger.info(
            f"Jail vote initiated for user {user.id} ({args[0]}) in chat {message.chat.id}"
        )
        if await vote.vote(
            message, client, f"Should the user {args[0]} be sent to jail?", 3
        ):
            users_in_jail_time[(message.chat.id, user.id)] = (
                datetime.datetime.now() + datetime.timedelta(minutes=15)
            )
            logger.info(
                f"User {user.id} ({args[0]}) sent to jail in chat {message.chat.id}. Jail status: {users_in_jail_time}"
            )
            await message.reply(f"The user {args[0]} has been sent to jail.")
        else:
            logger.info(
                f"Jail vote failed for user {user.id} ({args[0]}) in chat {message.chat.id}"
            )
            await message.reply("The vote failed")

    @app.on_message()
    async def go_to_jail(client: Client, message: Message):
        """
        Monitor all messages and delete messages from users in jail.

        This handler runs on every message and checks if the sender is in jail.
        If they are, their message is deleted. If their sentence has expired,
        they are automatically released from jail.

        Args:
            client: Pyrogram client instance
            message: Any message sent in the chat
        """
        try:
            if (
                users_in_jail_time[(message.chat.id, message.from_user.id)]
                < datetime.datetime.now()
            ):
                users_in_jail_time.pop((message.chat.id, message.from_user.id))
                logger.info(
                    f"User {message.from_user.id} ({message.from_user.first_name}) has been released from jail in chat {message.chat.id}"
                )
        except Exception:
            return
        try:
            logger.debug(
                f"User {message.from_user.id} ({message.from_user.first_name}) tried to escape from jail, deleting message {message.id} in chat {message.chat.id}"
            )
            await client.delete_messages(
                chat_id=message.chat.id, message_ids=message.id
            )
        except Exception as e:
            logger.warning(
                f"Failed to delete message {message.id} from jailed user {message.from_user.id}: {e}"
            )
