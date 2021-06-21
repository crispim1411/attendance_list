import asyncio 
import discord
from discord.ext import commands

import config
from attendance import process_data, insert_to_database

client = commands.Bot(command_prefix = config.PREFIX)
            
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith(config.PREFIX):
        await process_data(message)

@client.event
async def on_reaction_add(reaction, user):
    channel = client.get_channel(reaction.message.channel.id)
    message = reaction.message
    itens = message.content.split('**')
    reaction = str(reaction).encode('unicode-escape')

    if len(itens) > 1:
        current_event = itens[1]

        if config.BOT not in str(user):
            if reaction == config.EMOJI.encode('unicode-escape'):
                await insert_to_database(message, user.mention, current_event)
            
client.run(config.TOKEN)
