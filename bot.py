import discord
import asyncio 

import config
from attendance import process_data

client = commands.Bot(command_prefix = config.PREFIX)
attendance_list = {}
            
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    global attendance_list
    if message.author == client.user:
        return

    if message.content.startswith(config.PREFIX):
        await process_data(message, attendance_list)

@client.event
async def on_reaction_add(reaction, user):
    global attendance_list

    channel = client.get_channel(reaction.message.channel.id)
    itens = reaction.message.content.split('**')
    reaction = str(reaction).encode('unicode-escape')

    if len(itens) > 1:
        current_event = itens[1]

        if config.BOT not in str(user):
            if reaction == config.EMOJI.encode('unicode-escape'):
                # inserção no banco
                attendance_list[current_event].append(user.mention)
                await channel.send(f"{user.mention} inscrito(a) em {current_event}")
            
client.run(config.TOKEN)
