from pyrogram import Client, filters
from pyrogram.types import Message
import gradio_client
from PIL import Image
import os
import asyncio
from random import random

def register_createGrup_command(app: Client):
    @app.on_message(filters.command("god_is_dead"))
    async def createGrup(client: Client, message: Message):
        # секретная функция
        print("god_is_dead command received")
        # берем аргументы
        args = message.text.split()[1:]
        await message.reply("подождите немного, это займет некоторое время...")
        # объединяем аргументы
        text = ''.join([i+" " for i in args])
        # подключаем апи
        async def grclin():
            return gradio_client.Client("stabilityai/stable-diffusion-3-medium")
        cl = await grclin()
        try:
            # выбираем животное
            word =""
            a = random()
            if a <=0.2:
                word = "fox"
            elif 0.2< a<=0.4:
                word = "wolf"
            elif 0.4<a<=0.6:
                word = "tiger"
            elif 0.6<a<=0.8:
                word = "pigeon"
            else:
                word = "cat"
            print(word)
            # это функция срабатывала очень долго и замораживала все остальные функции, пришлось выносить в отдельную async функцию
            async def async_predict(word, text):
                return await asyncio.to_thread(cl.predict,
                                            prompt=f"furry-{word} muscular 3d hentai " + text,
                                            negative_prompt="",
                                            randomize_seed=True,
                                            width=1024,
                                            height=1024,
                                            guidance_scale=5,
                                            num_inference_steps=28,
                                            api_name="/infer")
            result = await async_predict(word, text)
        except Exception as e:
            await message.reply(f"Произошла непредвиденная ошибка:{e}")
        print(result)
        # переводим картинку из формата .webp
        image = Image.open(result[0])
        image.save('output.png', 'png')
        await client.send_photo(message.chat.id,"output.png")
        # удаляем все что нагенерили
        os.remove("output.png")
        os.remove(result[0])