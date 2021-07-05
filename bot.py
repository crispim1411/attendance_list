import os
import asyncio 
import discord
from discord.ext import commands

import attendance
try:
    from config import config
except:
    config = os.environ

client = commands.Bot(command_prefix = config['PREFIX'])
            
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith(config['PREFIX']):
        await attendance.process_data(message)

@client.event
async def on_reaction_add(reaction, user):
    if len(reaction.message.embeds) == 0:
        itens = reaction.message.content.split('**')
    else:
        embed_description = reaction.message.embeds[0].description
        itens = embed_description.split('**')
    message = reaction.message
    reaction = str(reaction).encode('unicode-escape')
    if len(itens) > 1:
        current_event = itens[1]

        if config['BOT'] not in str(user):
            if reaction == attendance.CHECK.encode('unicode-escape'):
                await attendance.insert_to_event(message, user.name, user.mention, current_event)
            elif reaction == attendance.CROSS.encode('unicode-escape'):
                if message.embeds[0].title == "Excluir evento":
                    await attendance.remove_event(message, current_event)
                else:
                    await attendance.remove_from_event(message, user.name, user.mention, current_event)
            
client.run(config['TOKEN'])
