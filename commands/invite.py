"""
Invite command module for the Telegram bot.

Allows users to vote on sending an invite link to the person who started the vote.
If the vote passes, a new invite link is created and sent to the user.
"""

import json

from pyrogram import Client, filters
from pyrogram.types import Message

import vote


def register_invite_command(app: Client):
    """
    Register invite command handler with the Pyrogram client.

    Registers the /invite command which creates a vote to send an invite link
    to the user who initiated the vote.

    Args:
        app: Pyrogram Client instance to register handlers with
    """

    @app.on_message(filters.command("invite"))
    async def invite(client: Client, message: Message):
        """
        Handle /invite command to vote on sending an invite link.

        Creates a poll to vote on sending an invite link to the user
        who started the vote. If the vote passes, a new invite link is
        created and sent to the user via private message.

        Usage: /invite

        Args:
            client: Pyrogram client instance
            message: The message containing the invite command
        """
        print("invite command received")
        # Get function parameters
        args = message.text.split()[1:]
        # Check for correct usage
        if len(args) > 0:
            await message.reply(
                "Ouch, you wrote something wrong. Use /help invite to learn how to use this function."
            )
            return
        if await vote.vote(
            message,
            client,
            f"Should an invite link be sent to {message.from_user.first_name}?",
            60 * 60 * 12,
        ):
            # Adding
            try:
                link_json = await client.create_chat_invite_link(message.chat.id)
                link = dict(json.loads(str(link_json)))["invite_link"]
                await message.reply(
                    f"An invitation has been sent to {message.from_user.first_name}"
                )
                # Send a message to the person who started the vote
                await client.send_message(
                    chat_id=message.from_user.id, text=f"Join here --> {link}"
                )
            except Exception as e:
                await message.reply_text(f"An error occurred: {e}")
        else:
            await message.reply("The vote failed")
