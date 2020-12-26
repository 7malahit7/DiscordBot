import discord
import Config
from discord import utils
from discord.ext import commands

Bot = commands.Bot( command_prefix = '.')


@Bot.event
async def on_ready():
    print('Bot Connected')

@Bot.event
async def on_message(message):
    if message.author == Bot.user:
        return
    else:
        content = message.content.split()
        for word in content:
            if word in Config.BanWord:
                await message.delete()
                await message.author.send(f'{ message.author.name }, не стоит такое писать :)')
                print('Automoderation working successfully')
    await Bot.process_commands(message)




Bot.run(Config.Token)
