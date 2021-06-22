import os
import discord
from discord.utils import get

import database

config = os.environ

CHECK = '\U00002705'
CROSS = '\U0000274c'
HELP =  "Listar os eventos cadastrados\n" \
        "```#listar```\n" \
        "Para cadastrar um novo evento" \
        "```#criar <nome do evento>```\n" \
        "Para reabrir inscrições de um evento\n" \
        "```#inscrever <nome do evento>```\n" \
        "Para listar os inscritos de um evento\n" \
        "```#listar <nome do evento>```\n" \
        "Para realizar chamada de um evento\n" \
        "```#chamada <nome do evento>```\n" \
        "Para cancelar inscrição em um evento\n" \
        "```#sair <nome do evento>```\n" \
        "Para excluir um evento\n" \
        "```#excluir <nome do evento>```\n" \
        "**CRISPY CORPORATIONS**\n" 

async def process_data(message):
    itens = message.content.split(' ')

    if message.content == config['PREFIX'] or message.content.startswith(config['PREFIX'] + 'help'):
        await message.channel.send(HELP)
        return

    if len(itens) == 1 and message.content.startswith(config['PREFIX'] + 'eventos'):
        await message.channel.send('Eventos cadastrados: ')
        events = database.find_all_events()
        if len(events) == 0:
            await message.channel.send('- Não há eventos cadastrados -')
        for event in events:
            await message.channel.send(f"- {event.name}")
        return

    content = ' '.join(itens[1:])

    if message.content.startswith(config['PREFIX'] + 'novo'):
        result = database.insert_event(content)
        if result == False:
            await message.channel.send(f'Este evento já está cadastrado.')
        else:
            msg = await message.channel.send(f'Interaja aqui para se inscrever na lista de alunos de **{content}**')
            await msg.add_reaction(CHECK)

    elif message.content.startswith(config['PREFIX'] + 'inscrever'):
        evento = database.find_event(content)
        if evento:
            msg = await message.channel.send(f'Interaja aqui para se inscrever na lista de alunos de **{content}**')
            await msg.add_reaction(CHECK)
        else:
            await message.channel.send(f'Este evento não está cadastrado. Use o comando #novo para inserir um novo evento.')

    elif message.content.startswith(config['PREFIX'] + 'chamada'):
        if database.find_event(content) == None:
            await message.channel.send("Evento não cadastrado.")
            return

        users = database.find_event_users(content)
        if len(users) == 0:
            await message.channel.send("Não há alunos inscritos.")
        for i, user in enumerate(users, start=1):
            await message.channel.send(f'{i}) {user.mention}')

    elif message.content.startswith(config['PREFIX'] + 'listar'):
        if database.find_event(content) == None:
            await message.channel.send("Evento não cadastrado.")
            return

        users = database.find_event_users(content)
        if len(users) == 0:
            await message.channel.send("Não há alunos inscritos.")
        for i, user in enumerate(users, start=1):
            await message.channel.send(f'{i}) {user.name}')

    elif message.content.startswith(config['PREFIX'] + 'sair'):
        evento = database.find_event(content)
        if evento:
            msg = await message.channel.send(f'Interaja aqui para retirar seu nome da lista de alunos de **{content}**')
            await msg.add_reaction(CROSS)
        else:
            await message.channel.send(f'Este evento não está cadastrado.')

    elif message.content.startswith(config['PREFIX'] + 'excluir'):
        result = database.delete_event(content)
        if result == False:
            await message.channel.send(f'Este evento não está cadastrado.')
        else:
            await message.channel.send(f'Evento removido.')
    
    else:
        await message.channel.send("Comando incorreto. Use #help para ver os comandos.")

async def insert_to_event(message, name, mention, event):
    result = database.insert_user(name, mention, event)
    if result == False:
        await message.channel.send("Você já está inscrito nessa aula.")
    else:
        await message.channel.send(f"{name} inscrito(a) em {event}")

async def remove_from_event(message, name, mention, event):
    result = database.delete_user(mention, event)
    if result == False:
        await message.channel.send("Não foi possível remover a inscrição.")
    else:
        await message.channel.send(f"{name} removido de {event}")