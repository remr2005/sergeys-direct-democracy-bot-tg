import json

from pyrogram import Client, filters
from pyrogram.types import Message

import vote


def register_invite_command(app: Client):
    @app.on_message(filters.command("invite"))
    async def invite(client: Client, message: Message):
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
