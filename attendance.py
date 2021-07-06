import os
from discord import Embed

import database
try:
    from config import config
except:
    config = os.environ

# Emojis
CHECK = '\U00002705'
CROSS = '\U0000274c'
WARN  = '\U000026A0'
# Tempo auto delete
DELETE_ERROR = 30
DELETE_WARN  = 60
# Cores
RED     = 0xf83629
YELLOW  = 0xe7f337
BLUE    = 0x538fdf
GREEN   = 0x6dc22c
# Mensagens
LOADING = "carregando..."


async def process_data(message):
    itens = message.content.split(' ')

    if message.content == config['PREFIX'] or message.content == config['PREFIX'] + 'help':
        embed_message = Embed(title="Comandos", color=BLUE)
        embed_message.add_field(name="Listar os eventos cadastrados", value="```#listar```", inline=False)
        embed_message.add_field(name="Cadastrar um novo evento", value="```#criar <nome do evento>```", inline=False)
        embed_message.add_field(name="Reabrir inscrições de um evento", value="```#inscrever <nome do evento>```", inline=False)
        embed_message.add_field(name="Listar os inscritos de um evento", value="```#listar <nome do evento>```", inline=False)
        embed_message.add_field(name="Realizar chamada de um evento", value="```#chamada <nome do evento>```", inline=False)
        embed_message.add_field(name="Cancelar inscrição em um evento", value="```#sair <nome do evento>```", inline=False)
        embed_message.add_field(name="Excluir um evento", value="```#excluir <nome do evento>```", inline=False)
        embed_message.set_footer(
            text="CRISPY CORPORATIONS", 
            icon_url="https://static.wikia.nocookie.net/digimon-adventure5140/images/f/fd/Digivice_tri.png/revision/latest?cb=20170328025147")
        await message.channel.send(embed = embed_message)
        return

    if len(itens) == 1:
        if message.content == config['PREFIX'] + 'listar':
            embed_message = Embed(title="Eventos cadastrados", color=YELLOW)
            msg = await message.channel.send(embed=embed_message)
            events = database.find_all_events()
            if len(events) == 0:
                embed_message.description = "- Não há eventos cadastrados -"
                await msg.edit(embed=embed_message)
                return

            embed_message.add_field(name="Eventos", value=LOADING, inline=True)
            embed_message.add_field(name="Inscritos", value="-", inline=True)
            await msg.edit(embed=embed_message)

            description = LOADING
            counter_text = ""
            embed_dict = embed_message.to_dict()
            for event in events:
                if description == LOADING:
                    description = f"{event[1]}\n" + LOADING
                else:
                    items = description.split(LOADING)
                    description = items[0] + f"{event[1]}\n" + LOADING

                num_users = database.count_event_users(event[1])
                counter_text += f"{num_users}\n"
                embed_dict['fields'][0]['value'] = description
                embed_dict['fields'][1]['value'] = counter_text
                await msg.edit(embed=Embed.from_dict(embed_dict))
            
            items = description.split(LOADING)
            embed_dict['fields'][0]['value'] = items[0]
            await msg.edit(embed=Embed.from_dict(embed_dict))
            
        else:
            description = "Comando incorreto. Use #help para ver os comandos."
            await message.channel.send(
                embed = Embed(title="Aviso", description=description, color=RED), 
                delete_after = DELETE_ERROR)

    else:
        content = ' '.join(itens[1:])

        if message.content.startswith(config['PREFIX'] + 'criar '):
            result = database.insert_event(content)
            if result == False:
                description = "Este evento já está cadastrado."
                await message.channel.send(
                    embed = Embed(title="Aviso", description=description, color=RED), 
                    delete_after = DELETE_ERROR)
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
                    embed = Embed(title="Aviso", description=description, color=RED), 
                    delete_after = DELETE_ERROR)

        elif message.content.startswith(config['PREFIX'] + 'chamada '):
            if database.find_event(content) == None:
                description = "Este evento não está cadastrado"
                await message.channel.send(
                    embed = Embed(title="Aviso", description=description, color=RED), 
                    delete_after = DELETE_ERROR)
                return

            users = database.find_event_users(content)
            description = LOADING
            embed_message = Embed(title=f"Chamada {content}", description=description, color=YELLOW)
            msg = await message.channel.send(embed=embed_message)
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
                    embed = Embed(title="Aviso", description=description, color=RED), 
                    delete_after = DELETE_ERROR)
                return

            users = database.find_event_users(content)
            description = LOADING
            embed_message = Embed(title=f"Listagem {content}", description=description, color=YELLOW)
            msg = await message.channel.send(embed=embed_message)
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
                embed_message.add_field(name="Removidos", value="-", inline=False)
                msg = await message.channel.send(embed=embed_message)
                await msg.add_reaction(CROSS)
            else:
                description = "Este evento não está cadastrado"
                await message.channel.send(
                    embed = Embed(title="Aviso", description=description, color=RED), 
                    delete_after = DELETE_ERROR)

        elif message.content.startswith(config['PREFIX'] + 'excluir '):
            result = database.find_event(content)
            if result == None:
                description = "Este evento não está cadastrado"
                await message.channel.send(
                    embed = Embed(title="Aviso", description=description, color=RED), 
                    delete_after = DELETE_ERROR)
            else:
                description = f"{WARN}Atenção{WARN}\nAo confirmar **{content}** será deletado"
                msg = await message.channel.send(
                    embed = Embed(title="Excluir evento", description=description, color=YELLOW),
                    delete_after = DELETE_WARN)
                await msg.add_reaction(CROSS)

        else:
            description = "Comando incorreto. Use #help para ver os comandos"
            await message.channel.send(
                embed = Embed(title="Aviso", description=description, color=RED), 
                delete_after = DELETE_ERROR)

async def insert_to_event(message, name, mention, event):
    if database.find_event(event) == None:
        description = "Este evento não está cadastrado"
        await message.channel.send(
            embed = Embed(title="Aviso", description=description, color=RED), 
            delete_after = DELETE_ERROR)
        return

    result = database.insert_user(name, mention, event)
    if result == False:
        description = f"**{name}** já possui inscrição em **{event}**"
        await message.channel.send(
            embed = Embed(title="Aviso", description=description, color=RED), 
            delete_after = DELETE_ERROR)
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
        await message.channel.send(
            embed = Embed(title="Aviso", description=description, color=RED),
            delete_after = DELETE_ERROR)
        return

    result = database.delete_user(mention, event)
    if result == False:
        description = f"**{name}** não possui inscrição em **{event}**"
        await message.channel.send(
            embed = Embed(title="Aviso", description=description, color=RED),
            delete_after = DELETE_ERROR)
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
        description = "Não foi possível remover o evento"
        await message.channel.send(
            embed = Embed(title="Aviso", description=description, color=RED), 
            delete_after = DELETE_ERROR)
    else:
        description = "Evento removido com sucesso"
        await message.channel.send(
            embed = Embed(title=f"Excluir evento {CHECK}", description=description, color=GREEN), 
            delete_after = DELETE_WARN)
