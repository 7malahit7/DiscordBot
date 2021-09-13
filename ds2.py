#============ || import ||===============#
import discord
import Config
from discord import utils
from discord.ext import commands
import asyncio
import json
#============ || main ||===============#

Bot = commands.Bot( command_prefix = '-', intents = discord.Intents.all())

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
async def mute(ctx, member: discord.Member, time:int,sec:str,reason1="Не указана", reason2="",reason3="", reason4="" , reason5="", reason6="", reason7="", reason8=""):
    while True:
        mute_role = discord.utils.get( ctx.message.guild.roles, id = 792454894417608744) #получаемая роль
        dmute_role = discord.utils.get( ctx.message.guild.roles, id = 790995360100515842) #удаляемая роль

        time1 = time
        if sec == "s":
            time,unit = time," секунд"
        elif sec == "m":
            time,unit = time*60," минут"
        elif sec == "h":
            time,unit = time*60*60," часов"
        elif sec == "d":
            time,unit = time*60*60*24," дней"
        else:
            emb2 = discord.Embed(title="Ошибка", color = 0xff0000)
            emb2.add_field(name="Tupoy moder...", value="Вы не указали единицу измерения времени [ s / m / h / d ]", inline=False)
            await ctx.send(embed=emb2)
            break

        emb = discord.Embed(title="Мут", color = 0xff0000)
        emb.add_field(name="Moдератор", value=ctx.message.author.mention, inline=False)
        emb.add_field(name="Нарушитель", value=member.mention, inline=False)
        emb.add_field(name="Причина", value=reason1+" "+reason2+" "+reason3+" "+reason4+" "+reason5+" "+reason6+" "+reason7+" "+reason8+" ", inline = False)
        emb.add_field(name="Время", value=str(time1)+unit, inline=False)
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
        break

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
async def clear(ctx, amount = 20):
    amount = amount + 1
    await ctx.channel.purge( limit = amount )

@Bot.command()
@commands.has_permissions(administrator=True, manage_roles=True)
async def reactrole(ctx, emoji, role: discord.Role, *, message):

    emb = discord.Embed(description=message)
    msg = await ctx.channel.send(embed=emb)
    await msg.add_reaction(emoji)

    with open('reactrole.json') as json_file:
        data = json.load(json_file)

        new_react_role = {'role_name': role.name,
        'role_id': role.id,
        'emoji': emoji,
        'message_id': msg.id}

        data.append(new_react_role)

    with open('reactrole.json', 'w') as f:
        json.dump(data, f, indent=4)
@Bot.event
async def on_raw_reaction_add(payload):

    if payload.member.bot:
        pass
    else:
        with open('reactrole.json') as react_file:
            data = json.load(react_file)
            for x in data:
                if x['emoji'] == payload.emoji.name:
                    role = discord.utils.get(Bot.get_guild(payload.guild_id).roles, id=x['role_id'])
                    await payload.member.add_roles(role)
                    print("ok")


@Bot.event
async def on_raw_reaction_remove(payload):
    with open('reactrole.json') as react_file:
        data = json.load(react_file)
        for x in data:
            if x['emoji'] == payload.emoji.name:
                role = discord.utils.get(Bot.get_guild(payload.guild_id).roles, id=x['role_id'])
                await Bot.get_guild(payload.guild_id).get_member(payload.user_id).remove_roles(role)
                print("ok")


#============ || start ||===============#

Bot.run(Config.Token)

