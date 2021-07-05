import os
from discord import Embed

import database
try:
    from config import config
except:
    config = os.environ

CHECK = '\U00002705'
CROSS = '\U0000274c'
DELETE_WARN = 60
DELETE_CALL = 120
RED = 0xf83629
YELLOW = 0xe7f337
BLUE = 0x538fdf
HELP =  "Para listar os eventos cadastrados\n" \
        "```#listar```\n" \
        "Para cadastrar um novo evento\n" \
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
        "```#excluir <nome do evento>```\n\n" \
        "**CRISPY CORPORATIONS**\n" 
LOADING = "carregando..."

async def process_data(message):
    itens = message.content.split(' ')

    if message.content == config['PREFIX'] or message.content == config['PREFIX'] + 'help':
        await message.channel.send(
            embed = Embed(title="Comandos", description=HELP, color=BLUE))
        return

    if len(itens) == 1:
        if message.content == config['PREFIX'] + 'listar':
            description = LOADING
            embed_message = Embed(title="Eventos cadastrados", description=description, color=YELLOW)
            msg = await message.channel.send(embed=embed_message)
            
            events = database.find_all_events()
            if len(events) == 0:
                embed_message.description = "- Não há eventos cadastrados -"
                await msg.edit(embed=embed_message)
                return

            for event in events:
                if description == LOADING:
                    description = f"{event[1]}\n" + LOADING
                else:
                    items = description.split(LOADING)
                    description = items[0] + f"{event[1]}\n" + LOADING
                embed_message.description = description
                await msg.edit(embed=embed_message)

            items = description.split(LOADING)
            embed_message.description = items[0]
            await msg.edit(embed=embed_message)
            
        else:
            description = "Comando incorreto. Use #help para ver os comandos."
            await message.channel.send(
                embed=Embed(title="Aviso", description=description, color=RED), 
                delete_after=DELETE_WARN)

    else:
        content = ' '.join(itens[1:])

        if message.content.startswith(config['PREFIX'] + 'criar '):
            result = database.insert_event(content)
            if result == False:
                description = "Este evento já está cadastrado."
                await message.channel.send(
                    embed=Embed(title="Aviso", description=description, color=RED), 
                    delete_after=DELETE_WARN)
            else:
                description = f"Interaja aqui para se inscrever na lista de **{content}**"
                embed_message = Embed(title="Novo evento", description=description, color=YELLOW)
                embed_message.add_field(name="Inscritos", value="-", inline=False)
                msg = await message.channel.send(embed=embed_message)
                await msg.add_reaction(CHECK)

        elif message.content.startswith(config['PREFIX'] + 'inscrever '):
            event = database.find_event(content)
            if event:
                description = f"Interaja aqui para se inscrever na lista de **{content}**"
                embed_message = Embed(title="Inscrição", description=description, color=YELLOW)
                embed_message.add_field(name="Inscritos", value="-", inline=False)
                msg = await message.channel.send(embed=embed_message)
                await msg.add_reaction(CHECK)
            else:
                description = "Este evento não está cadastrado"
                await message.channel.send(
                    embed=Embed(title="Aviso", description=description, color=RED), 
                    delete_after=DELETE_WARN)

        elif message.content.startswith(config['PREFIX'] + 'chamada '):
            if database.find_event(content) == None:
                description = "Este evento não está cadastrado"
                await message.channel.send(
                    embed=Embed(title="Aviso", description=description, color=RED), 
                    delete_after=DELETE_WARN)
                return

            users = database.find_event_users(content)
            description = LOADING
            embed_message = Embed(title=f"Chamada {content}", description=description, color=YELLOW)
            msg = await message.channel.send(embed=embed_message, delete_after=DELETE_CALL)
            if len(users) == 0:
                embed_message.description = "- Não há inscritos -"
                await msg.edit(embed=embed_message)
                return

            for i, user in enumerate(users, start=1):
                if description == LOADING:
                    description = f"{i}) {user[2]}\n" + LOADING
                else:
                    items = description.split(LOADING)
                    description = items[0] + f"{i}) {user[2]}\n" + LOADING
                embed_message.description = description
                await msg.edit(embed=embed_message)

            items = description.split(LOADING)
            embed_message.description = items[0]
            await msg.edit(embed=embed_message)

        elif message.content.startswith(config['PREFIX'] + 'listar '):
            if database.find_event(content) == None:
                description = "Este evento não está cadastrado"
                await message.channel.send(
                    embed=Embed(title="Aviso", description=description, color=RED), 
                    delete_after=DELETE_WARN)
                return

            users = database.find_event_users(content)
            description = LOADING
            embed_message = Embed(title=f"Listagem {content}", description=description, color=YELLOW)
            msg = await message.channel.send(embed=embed_message, delete_after=DELETE_CALL)
            if len(users) == 0:
                embed_message.description = "- Não há inscritos -"
                await msg.edit(embed=embed_message)
                return

            for i, user in enumerate(users, start=1):
                if description == LOADING:
                    description = f"{i}) {user[1]}\n"
                else:
                    items = description.split(LOADING)
                    description = items[0] + f"{i}) {user[1]}\n" + LOADING
                embed_message.description = description
                await msg.edit(embed=embed_message)
            
            items = description.split(LOADING)
            embed_message.description = items[0]
            await msg.edit(embed=embed_message)

        elif message.content.startswith(config['PREFIX'] + 'sair '):
            evento = database.find_event(content)
            if evento:
                description = f"Interaja aqui para retirar seu nome da lista de **{content}**"
                embed_message = Embed(title=f"Remover inscrição", description=description, color=YELLOW)
                embed_message.add_field(name="Removidos", value="-", sinline=False)
                msg = await message.channel.send(embed=embed_message)
                await msg.add_reaction(CROSS)
            else:
                description = "Este evento não está cadastrado"
                await message.channel.send(
                    embed=Embed(title="Aviso", description=description, color=RED), 
                    delete_after=DELETE_WARN)

        elif message.content.startswith(config['PREFIX'] + 'excluir '):
            result = database.find_event(content)
            if result == None:
                description = "Este evento não está cadastrado"
                await message.channel.send(
                    embed=Embed(title="Aviso", description=description, color=RED), 
                    delete_after=DELETE_WARN)
            else:
                description = f"Confirme a remoção do evento **{content}**"
                msg = await message.channel.send(
                    embed=Embed(title="Excluir evento", description=description, color=YELLOW))
                await msg.add_reaction(CROSS)

        else:
            description = "Comando incorreto. Use #help para ver os comandos"
            await message.channel.send(
                embed=Embed(title="Aviso", description=description, color=RED), 
                delete_after=DELETE_WARN)

async def insert_to_event(message, name, mention, event):
    if database.find_event(event) == None:
        description = "Este evento não está cadastrado"
        embed_message = Embed(title="Aviso", description=description, color=RED)
        await message.channel.send(embed=embed_message, delete_after=DELETE_WARN)
        return

    result = database.insert_user(name, mention, event)
    if result == False:
        description = f"**{name}** já possui inscrição em **{event}**"
        embed_message = Embed(title="Aviso", description=description, color=RED)
        await message.channel.send(embed=embed_message, delete_after=DELETE_WARN)
    else:
        embed_message = message.embeds[0]
        embed_dict = embed_message.to_dict()
        edited_text = embed_dict['fields'][0]['value']
        if edited_text == "-":
            edited_text = ""
        edited_text += f"\n{name}"
        embed_dict['fields'][0]['value'] = edited_text
        await message.edit(embed=Embed.from_dict(embed_dict))

async def remove_from_event(message, name, mention, event):
    if database.find_event(event) == None:
        description = "Este evento não está cadastrado"
        embed_message = Embed(title="Aviso", description=description, color=RED)
        await message.channel.send(embed=embed_message, delete_after=DELETE_WARN)
        return

    result = database.delete_user(mention, event)
    if result == False:
        description = f"**{name}** não possui inscrição em **{event}**"
        embed_message = Embed(title="Aviso", description=description, color=RED)
        await message.channel.send(embed=embed_message, delete_after=DELETE_WARN)
    else:
        embed_message = message.embeds[0]
        embed_dict = embed_message.to_dict()
        edited_text = embed_dict['fields'][0]['value']
        if edited_text == "-":
            edited_text = ""
        edited_text += f"\n{name}"
        embed_dict['fields'][0]['value'] = edited_text
        await message.edit(embed=Embed.from_dict(embed_dict))

async def remove_event(message, event):
    # colocar novo campo criador do evento
    # checar se tem permissão para deletar
    result = database.delete_event(event)
    if result == False:
        description = f"Não foi possível remover o evento"
        embed_message = Embed(title="Aviso", description=description, color=RED)
        await message.channel.send(embed=embed_message, delete_after=DELETE_WARN)
    else:
        description = f"Evento removido com sucesso"
        embed_message = Embed(title="Excluir evento", description=description, color=YELLOW)
        await message.channel.send(embed=embed_message, delete_after=DELETE_WARN)
