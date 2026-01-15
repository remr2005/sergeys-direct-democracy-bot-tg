"""
Voting module for the direct democracy bot.

This module provides functionality to create polls, monitor voting progress,
and determine voting results based on participation thresholds.
"""

import asyncio

from pyrogram import Client
from pyrogram.types import Message


async def vote(
    message: Message, client: Client, question: str, time: int = 259200
) -> bool:
    """
    Create and manage a voting poll in a Telegram chat.

    The voting ends when either:
    - More than 60% of chat members have voted, or
    - The specified time limit is reached

    Args:
        message: The Telegram message that triggered the vote
        client: Pyrogram client instance
        question: The question to ask in the poll
        time: Maximum voting time in seconds (default: 259200 = 3 days)

    Returns:
        True if "Да" (Yes) votes >= "Нет" (No) votes, False otherwise
    """
    try:
        poll_message = await client.send_poll(
            chat_id=message.chat.id,
            question=question,
            options=["Да", "Нет"],
            is_anonymous=False,
        )
        b = 0
        async for m in client.get_chat_members(message.chat.id):
            b += 1
        print(f"Голосование {poll_message.id} стартовало")
        while True:
            await asyncio.sleep(1)
            time -= 1
            if time <= 0:
                break
            poll_message = await client.get_messages(message.chat.id, poll_message.id)
            results = {
                option.text: option.voter_count for option in poll_message.poll.options
            }
            if (results["Да"] + results["Нет"]) > int(b * 0.6):
                break
        print(f"Голосование {poll_message.id} окончено")
        if results["Да"] >= results["Нет"]:
            return True
        return False
    except Exception as e:
        print(f"Exception occurred: {str(e)}")
        return False
