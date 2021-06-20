import config
import discord

async def process_data(message, attendance_list):
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

    if message.content.startswith(config.PREFIX + 'novo'):
        attendance_list[content] = []
        msg = await message.channel.send(f'Interaja aqui para se inscrever na lista de alunos de **{content}**')
        await msg.add_reaction(config.EMOJI)

    elif message.content.startswith(config.PREFIX + 'chamada'):
        if content not in attendance_list.keys():
            await message.channel.send("Evento não cadastrado.")
            return

        if len(attendance_list[content]) == 0:
            await message.channel.send("Não há alunos inscritos.")
        for i, user in enumerate(attendance_list[content], start=1):
            await message.channel.send(f'{i}) {user}')