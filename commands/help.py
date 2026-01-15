from pyrogram import Client, filters
from pyrogram.types import BotCommand, Message


def register_help_command(app: Client):
    # It's quite possible that there's some ridiculous nonsense written here, but I haven't figured out what to do with it yet
    @app.on_message(filters.command("setcommands"))
    async def set_commands(client, message):
        commands = [
            BotCommand("help", "Get help"),
            BotCommand("make_admin", "Give a user admin status through voting"),
            BotCommand(
                "remove_admin", "Remove admin status from a user through voting"
            ),
            BotCommand("kick", "Kick a user through voting"),
            BotCommand(
                "invite", "Send an invite link to the person who started the vote"
            ),
            BotCommand(
                "change_icon", "Change the group icon to the one suggested by the user"
            ),
            BotCommand("change_name", "Change the group name"),
            BotCommand("go_to_jail", "Send a user to jail for 15 minutes"),
        ]
        await client.set_bot_commands(commands)
        await message.reply("Commands successfully set!")

    # This is help... Wow
    @app.on_message(filters.command("help"))
    async def help(client: Client, message: Message):
        print("Help command received")
        args = message.text.split()[1:]
        if len(args) == 0:
            await message.reply("""List of all available commands:
                                make_admin
                                remove_admin
                                invite
                                kick
                                change_icon
                                change_name
and many other secret commands...
P.S. You can also check out the source code at https://github.com/remr2005/sergeys-direct-democracy-bot-tg.""")
        elif args[0] == "make_admin":
            await message.reply("""The /make_admin command creates a vote to give admin status.
Usage: /make_admin [user]
Example: /make_admin @example_user""")
        elif args[0] == "remove_admin":
            await message.reply("""The /remove_admin command creates a vote to remove admin status.
Usage: /remove_admin [user]
Example: /remove_admin @example_user""")
        elif args[0] == "kick":
            await message.reply("""The /kick command creates a vote to kick a user.
Usage: /kick [user]
Example: /kick @example_user""")
        elif args[0] == "invite":
            await message.reply("""The /invite command creates a vote to send an invite link to the person who started the vote.
Usage: /invite""")
        elif args[0] == "change_icon":
            await message.reply("""The /change_icon command creates a vote to change the group icon.
Usage: /change_icon (attach a photo to this message)""")
        elif args[0] == "change_name":
            await message.reply("""The /change_name command creates a vote to change the group name.
Usage: /change_name [some name]
Example: /change_name example""")
        elif args[0] == "go_to_jail":
            await message.reply("""The /go_to_jail command creates a vote to send a user to jail.
Usage: /go_to_jail [user]
Example: /go_to_jail @example""")
