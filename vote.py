"""
Voting module for the direct democracy bot.

This module provides functionality to create polls, monitor voting progress,
and determine voting results based on participation thresholds.
"""

import asyncio
import logging

from pyrogram import Client
from pyrogram.types import Message

logger = logging.getLogger(__name__)


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
        logger.info(
            f"Голосование {poll_message.id} стартовало в чате {message.chat.id}. Вопрос: '{question}'. Всего участников: {b}, порог участия: {int(b * 0.6)}"
        )
        while True:
            await asyncio.sleep(1)
            time -= 1
            poll_message = await client.get_messages(message.chat.id, poll_message.id)
            results = {
                option.text: option.voter_count for option in poll_message.poll.options
            }
            if time <= 0:
                logger.info(
                    f"Голосование {poll_message.id} окончено: достигнут лимит времени"
                )
                break
            if (results["Да"] + results["Нет"]) > int(b * 0.6):
                logger.info(
                    f"Голосование {poll_message.id} окончено: достигнут порог участия ({(results['Да'] + results['Нет'])}/{b} голосов)"
                )
                break
        logger.info(
            f"Голосование {poll_message.id} окончено. Результаты: Да={results.get('Да', 0)}, Нет={results.get('Нет', 0)}"
        )
        if results["Да"] >= results["Нет"]:
            return True
        return False
    except Exception as e:
        logger.error(f"Exception occurred in vote function: {str(e)}", exc_info=True)
        return False
