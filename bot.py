import discord
from discord.utils import get
from discord.ext import commands
import config
import asyncio 

BOT = 'Lista de chamada#1795' # trocar para #1795
AUTHORS = ['Crispim#8453', 'crispim2#6967']
EMOJI = '\U00002705'

client = commands.Bot(command_prefix = config.PREFIX)
attendance_list = {}
current_event = ""

async def process_data(message):
    global attendance_list
    global current_event
    
    itens = message.content.split(' ')

    if message.content.startswith(config.PREFIX + 'eventos'):
        await message.channel.send('Eventos cadastrados: ')
        for event in attendance_list.keys():
            await message.channel.send(event)
        return

    if len(itens) < 2:
        await message.channel.send("Por favor, digite o nome do evento.")
        return 
        
    content = ' '.join(itens[1:])
    current_event = content

    if message.content.startswith(config.PREFIX + 'novo'):
        attendance_list[current_event] = []
        msg = await message.channel.send('Interaja aqui para se inscrever na lista de alunos de {current_event}')
        await msg.add_reaction(EMOJI)

    elif message.content.startswith(config.PREFIX + 'chamada'):
        if current_event not in attendance_list.keys():
            await message.channel.send("Evento não cadastrado.")
            return

        if len(attendance_list[current_event]) == 0:
            await message.channel.send("Não há alunos inscritos.")
        for i, user in enumerate(attendance_list[current_event], start=1):
            await message.channel.send(f'{i}) {user}')
            
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
    global attendance_list
    global current_event

    channel = client.get_channel(reaction.message.channel.id)
    reaction = str(reaction).encode('unicode-escape')

    if str(user) != BOT:
        if reaction == EMOJI.encode('unicode-escape'):
            attendance_list[current_event].append(user.mention)
            await channel.send(f"{user.mention} inscrito(a) em {current_event}")
            
client.run(config.TOKEN)
