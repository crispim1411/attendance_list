import asyncio 
import discord
from discord.ext import commands
# imports do projeto 
import process_command
import send_message
from config import config
try:
    import credentials
    TOKEN = credentials.TOKEN
    BOT = credentials.BOT
except:
    import os
    TOKEN = os.environ['TOKEN']
    BOT = os.environ['BOT']

client = commands.Bot(command_prefix = config['PREFIX'])
            
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith(config['PREFIX']):
        await process_command.process_data(message)

@client.event
async def on_reaction_add(reaction, user):
    if len(reaction.message.embeds) == 1: #unico não embed é #chamada
        embed_description = reaction.message.embeds[0].description
        itens = embed_description.split('**')
    else:
        return

    message = reaction.message
    str_reaction = str(reaction).encode('unicode-escape')
    if len(itens) > 1:
        current_event = itens[1]

        if BOT not in str(user):
            if str_reaction == config['CHECK'].encode('unicode-escape'):
                await send_message.insert_user(message, user.name, user.mention, current_event)

            elif str_reaction == config['CROSS'].encode('unicode-escape'):
                if message.embeds[0].title == "Excluir evento":
                    await send_message.remove_event_response(message, user.mention, current_event)
                else:
                    await send_message.remove_subscription_reponse(message, user.name, user.mention, current_event)
            
client.run(TOKEN)
