"""
Kick command module for the Telegram bot.

Allows users to vote on kicking a member from the group.
If the vote passes, the user is temporarily banned for 1 minute.
"""

from datetime import datetime, timedelta

from pyrogram import Client, filters
from pyrogram.types import Message

import vote


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
        print("kick command received")
        # Get function parameters
        args = message.text.split()[1:]
        # Check for correct usage TODO make more fine-tuned admin settings
        if len(args) == 0 or len(args) > 1:
            await message.reply(
                "Ouch, you wrote something wrong. Use /help kick to learn how to use this function."
            )
            return
        # Get user ID
        user = await client.get_users(args[0][1:])
        if await vote.vote(
            message, client, f"Should the user {args[0]} be kicked?", 60 * 60 * 12
        ):
            # Kick
            try:
                # Time until the user will be banned (e.g., for 1 minute)
                await app.ban_chat_member(
                    message.chat.id, user.id, datetime.now() + timedelta(minutes=1)
                )
                await message.reply(f"The user {args[0]} has been kicked")
            except Exception as e:
                await message.reply_text(f"An error occurred: {e}")
        else:
            await message.reply("The vote failed")
