import discord
import Config
from discord import utils


intents = discord.Intents.all()

class MyClient(discord.Client):

    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def on_raw_reaction_add(self, payload):
        channel = self.get_channel(payload.channel_id)

    async def on_raw_reaction_add(self, payload):
        if payload.message_id == Config.MessageId or payload.message_id == Config.MessageId2:

            channel = self.get_channel(payload.channel_id) #канал
            message = await channel.fetch_message(payload.message_id) #сообщение
            member = utils.get(message.guild.members, id=payload.user_id) #User
            try:
                emoji = str(payload.emoji) # эмодзи юзера
                role = utils.get(message.guild.roles, id=Config.Roles[emoji])

                if(len([i for i in member.roles if i.id not in Config.ExcepRole]) <= Config.MaxCountRole):
                    await member.add_roles(role)
                    print('[Success] User {0.display_name} has accepted with role {1.name}'.format(member, role))
                else:
                    await message.remove_reaction(payload.emoji, member)
            finally:
                print()


    async def on_raw_reaction_remove(self, payload):
        if payload.message_id == Config.MessageId or payload.message_id == Config.MessageId2:
            channel = self.get_channel(payload.channel_id) #канал
            message = await channel.fetch_message(payload.message_id) #сообщение
            member = utils.get(message.guild.members, id=payload.user_id) #User
            try:
                emoji = str(payload.emoji) # эмодзи юзера
                role = utils.get(message.guild.roles, id=Config.Roles[emoji])

                if(len([i for i in member.roles if i.id not in Config.ExcepRole]) <= Config.MaxCountRole):
                    await member.remove_roles(role)
                    print('[Success] User {0.display_name} has disabled with role {1.name}'.format(member, role))
                else:
                    print('bruh')

            except KeyError as e:
                print('[Error], no role found for'+emoji)
            except Exception as e:
                print(repr(e))


#start
Client = MyClient(intents=intents)
Client.run(Config.Token)
