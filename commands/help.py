from pyrogram import Client, filters
from pyrogram.types import Message, BotCommand

def register_help_command(app: Client):
    # Вполне возможно, что тут написана ебейшая срань, но я пока не понял что мне с этим делать
    @app.on_message(filters.command("setcommands"))
    async def set_commands(client, message):
        commands = [
            BotCommand("help", "Получить помощь"),
            BotCommand("make_admin", "Дать пользователю админку в ходе голосования"),
            BotCommand("remove_admin", "Забрать у пользователя админку в ходе голосования"),
            BotCommand("kick", "Кикнуть пользователя в ходе голосования"),
            BotCommand("invite", "Кинуть инвайт-ссылку тому кто начал голосование"),
            BotCommand("change_icon", "Изменить аву группы, на ту что предложил юзер"),
            BotCommand("change_name", "Изменить название группы"),
        ]
        await client.set_bot_commands(commands)
        await message.reply("Команды успешно установлены!")
    # Это хелп... Вау
    @app.on_message(filters.command("help"))
    async def help(client: Client, message: Message):
        print("Help command received")
        args = message.text.split()[1:]
        if len(args)==0:
            await message.reply('''В общем, здрасте, наш ебейший сервак https://discord.gg/UEYQPsAuR4, а так же канал в котором есть новости о разработке и щитпост(его гораздо больше) https://t.me/churkopeiaForever. Список всех доступных команд:
                                make_admin
                                remove_admin
                                invite
                                kick
                                change_icon
                                change_name
а так же множество других, секретных команд...
P.S Вы так же можете посмотреть исходный код https://github.com/remr2005/sergeys-direct-democracy-bot-tg.''')
        elif args[0]=="make_admin":
            await message.reply("""Команда /make_admin, создание голосование по поводу выдачи админки.
Использование: /make_admin [user]
Пример: /make_admin @example_user""")
        elif args[0]=="remove_admin":
            await message.reply("""Команда /remove_admin, создание голосование по поводу отбирания админки.
Использование: /remove_admin [user]
Пример: /remove_admin @example_user""")
        elif args[0]=="kick":
            await message.reply("""Команда /kick, создание голосование по поводу кика пользователя.
Использование: /kick [user]
Пример: /kick @example_user""")
        elif args[0]=="invite":
            await message.reply("""Команда /invite, создание голосование по киданию ссылки инвайта, тому кто начал голосование.
Использование: /invite""")
        elif args[0]=="change_icon":
            await message.reply("""Команда /change_icon, создание голосование по изменнению авы группы.
Использование: /change_icon (прикрепите к этому сообщению какую то фотку)""")
        elif args[0]=="change_name":
            await message.reply("""Команда /change_name, создание голосование по изменнению названия группы.
Использование: /change_name [какое то название]
Пример: /change_name example""")
            

