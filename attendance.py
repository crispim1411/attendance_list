import discord

import config
from database import insert_user, insert_event
from database import find_event, find_all_events, find_event_users

async def process_data(message):
    itens = message.content.split(' ')

    if message.content.startswith(config.PREFIX + 'eventos'):
        await message.channel.send('Eventos cadastrados: ')
        events = find_all_events()
        if len(events) == 0:
            await message.channel.send('- Não há eventos cadastrados -')
        for event in events:
            await message.channel.send(f"- {event.name}")
        return

    if len(itens) < 2:
        await message.channel.send("Comando incorreto.")
        return 
        
    content = ' '.join(itens[1:])

    if message.content.startswith(config.PREFIX + 'novo'):
        insert_event(content)
        msg = await message.channel.send(f'Interaja aqui para se inscrever na lista de alunos de **{content}**')
        await msg.add_reaction(config.EMOJI)

    elif message.content.startswith(config.PREFIX + 'chamada'):
        if len(find_event(content)) == 0:
            await message.channel.send("Evento não cadastrado.")
            return

        users = find_event_users(content)
        if len(users) == 0:
            await message.channel.send("Não há alunos inscritos.")
        for i, user in enumerate(users, start=1):
            await message.channel.send(f'{i}) {user.name}')

def insert_to_database(user, event):
    insert_user(user, event)