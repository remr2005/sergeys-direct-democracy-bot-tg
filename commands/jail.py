"""
Jail command module for the Telegram bot.

Allows users to vote on sending a user to "jail" for 15 minutes.
Users in jail have their messages automatically deleted until their sentence ends.
"""

import datetime

from pyrogram import Client, filters
from pyrogram.types import Message

import vote

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
        print("jail command received")
        # Get function parameters
        args = message.text.split()[1:]
        # Check for correct usage TODO make more fine-tuned admin settings
        if len(args) == 0 or len(args) > 1:
            await message.reply(
                "Ouch, you wrote something wrong. Use /help go_to_jail to learn how to use this function."
            )
            return
        # Get user ID
        user = await client.get_users(args[0][1:])
        if await vote.vote(
            message, client, f"Should the user {args[0]} be sent to jail?", 3
        ):
            users_in_jail_time[(message.chat.id, user.id)] = (
                datetime.datetime.now() + datetime.timedelta(minutes=15)
            )
            print(users_in_jail_time)
            await message.reply(f"The user {args[0]} has been sent to jail.")
        else:
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
                print(
                    f"{message.from_user.id} has been released in chat {message.chat.id}"
                )
        except Exception:
            return
        try:
            print(f"{message.from_user.first_name} tried to escape from jail")
            await client.delete_messages(
                chat_id=message.chat.id, message_ids=message.id
            )
        except Exception as e:
            print(f"Failed to delete message {message.id}: {e}")
