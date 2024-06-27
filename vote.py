import asyncio
from pyrogram import Client
from pyrogram.types import Message

""" Передаёте message, client, ставить вопрос question по которому идет голосование, варианты голосования options и время в секундах time.
Функция возвращает True если голосование прошло успешно и False во всех иных случаях.
P.S Так что хуй вам, а не третья опция"""
async def vote(message: Message, client: Client,question: str, time: int=259200) -> bool:
        poll_message = await client.send_poll(
            chat_id=message.chat.id,
            question=question,
            options=["Да","Нет"],
            is_anonymous=False  # Устанавливаем False, если хотите, чтобы голосование было неанонимным
        )
        # TODO:пока что голосование идет ровно time секунд и никак иначе, нужно сделать автозавершения после n% проголосовавих
        await asyncio.sleep(time)
        results = {option.text: option.voter_count for option in poll_message.poll.options}
        # Пока что голосование всегда идет по принципу Да vs Нет, не вижу смысла это менять, но вообще было неплохло TODO: кастомное голосование
        if results["Да"] >= results["Нет"]:
                return True
        return False