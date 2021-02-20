#============ || import ||===============#
import discord
import Config
from discord import utils
from discord.ext import commands
import asyncio
#============ || main ||===============#

Bot = commands.Bot( command_prefix = '.')

@Bot.event #включение
async def on_ready():
    print('Bot Connected')

@Bot.event #автомодерация
async def on_message(message):
    if message.author == Bot.user:
        return
    else:
        content = message.content.split()
        for word in content:
            if word in Config.BanWord:
                await message.channel.send(f'{ message.author.name }, клоун ебучий')
                await message.delete()
                await message.author.send(f'{ message.author.name }, не стоит такое писать :)')
                print('Automoderation working successfully')
    await Bot.process_commands(message)

@Bot.command()#Мут
@commands.has_permissions( kick_members=True )
async def mute(ctx, member: discord.Member, time:int,reason,reason1="", reason2="",reason3="", reason4="" , reason5="", reason6="", reason7="", reason8=""):
    mute_role = discord.utils.get( ctx.message.guild.roles, id = 792454894417608744) #получаемая роль
    dmute_role = discord.utils.get( ctx.message.guild.roles, id = 790995360100515842) #удаляемая роль
    emb = discord.Embed(title="Мут", color = 0xff0000)
    emb.add_field(name="Moдератор", value=ctx.message.author.mention, inline=False)
    emb.add_field(name="Нарушитель", value=member.mention, inline=False)
    emb.add_field(name="Причина", value=reason+" "+reason1+" "+reason2+" "+reason3+" "+reason4+" "+reason5+" "+reason6+" "+reason7+" "+reason8+" ", inline = False)
    emb.add_field(name="Время", value=time, inline=False)
    await member.send(embed=emb)
    await member.add_roles(mute_role)
    await member.remove_roles(dmute_role)
    await ctx.send(embed=emb)
    print(f"{member.name} muted")
    emb1 = discord.Embed(title="Размут", color = 0x0afc37)
    emb1.add_field(name = f'был размучен', value=member.mention, inline=False)
    await asyncio.sleep(time)
    await member.add_roles(dmute_role)
    await member.remove_roles(mute_role)
    await ctx.send(embed=emb1)
    await member.send(embed=emb1)
    print(f"{member.name} unmuted")


@Bot.command()#Анмут
@commands.has_permissions( kick_members=True )
async def unmute(ctx, member: discord.Member ):
    dmute_role = discord.utils.get( ctx.message.guild.roles, id = 792454894417608744)#удаляемая роль
    mute_role = discord.utils.get( ctx.message.guild.roles, id = 790995360100515842)#получаемая роль
    emb = discord.Embed(title="Размут", color = 0x0afc37)
    emb.add_field(name = 'Был досроно размучен', value = member.mention)
    await member.add_roles(mute_role)
    await member.remove_roles(dmute_role)
    await ctx.send(embed=emb)
    await member.send(embed=emb)
    print(f"{member.name} UNmuted")

@Bot.command()#Анмут
@commands.has_permissions( kick_members=True )
async def clear(ctx, amount = 10):
    amount = amount + 1
    await ctx.channel.purge( limit = amount )


#============ || start ||===============#

Bot.run(Config.Token)
