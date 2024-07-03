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
        print("create_group command received")
        args = message.text.split()[1:]
        await message.reply("подождите немного, это займет некоторое время...")
        text = ''.join([i+" " for i in args])
        cl = gradio_client.Client("stabilityai/stable-diffusion-3-medium")
        try:
            word =""
            a = random()
            if a <=0.3:
                word = "fox"
            elif 0.3< a<=0.6:
                word = "wolf"
            elif 0.6<a<=0.9:
                word = "tiger"
            else:
                word = "cat"
            print(word)
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
            # result =  cl.predict(
            #         prompt=f"furry-{word} muscular 3d hentai "+text,
            #         negative_prompt="",
            #         randomize_seed=True,
            #         width=1024,
            #         height=1024,
            #         guidance_scale=5,
            #         num_inference_steps=28,
            #         api_name="/infer"
            # )
            result = await async_predict(word, text)
        except Exception as e:
            await message.reply(f"Произошла непредвиденная ошибка:{e}")
        print(result)
        image = Image.open(result[0])
        image.save('output.png', 'png')
        await client.send_photo(message.chat.id,"output.png")
        os.remove("output.png")
        os.remove(result[0])