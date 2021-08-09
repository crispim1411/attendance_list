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

import os
from random import choice
from discord import Embed
from discord_components import Button, ButtonStyle
from discord_components.component import Select, SelectOption
import database
try:
    from config import config
except:
    config = os.environ

async def help(message):
    embed_message = Embed(title="Comandos", color=BLUE)
    embed_message.add_field(name="Cadastrar um novo evento", 
        value=f"```*criar <nome do evento>```", inline=False)
    embed_message.add_field(name="Excluir um evento", 
        value=f"```{config['PREFIX']}excluir <nome do evento>```", inline=False)
    embed_message.add_field(name="Renomear evento", 
        value=f"```{config['PREFIX']}renomear <nome> - <novo nome>```", inline=False)
    embed_message.add_field(name="Listar os eventos cadastrados", 
        value=f"```{config['PREFIX']}eventos```", inline=False)
    embed_message.add_field(name="Listar os inscritos de um evento", 
        value=f"```{config['PREFIX']}info```", inline=False)
    embed_message.add_field(name="Realizar chamada de um evento", 
        value=f"```{config['PREFIX']}chamada```", inline=False)
    embed_message.add_field(name="Reabrir inscrições de um evento", 
        value=f"```{config['PREFIX']}inscrever```", inline=False)
    embed_message.add_field(name="Cancelar inscrição em um evento", 
        value=f"```{config['PREFIX']}sair```", inline=False)
    embed_message.add_field(name="Código do bot", 
        value=f"```{config['PREFIX']}source```", inline=False)
    embed_message.set_footer(
        text="CRISPY CORPORATIONS", 
        icon_url=config['ICON_URL'])
    await message.channel.send(embed = embed_message)

async def new_event(message, content):
    result = database.insert_event(content, message.author.mention, str(message.guild.id))
    if result == False:
        description = "Este evento já está cadastrado."
        await message.channel.send(
            embed = Embed(title="Aviso", description=description, color=RED), 
            delete_after = DELETE_ERROR)
    else:
        description = f"Interaja aqui para se inscrever na lista de **{content}**"
        embed_message = Embed(title="Novo evento", description=description, color=YELLOW)
        embed_message.add_field(name="Inscritos", value="-", inline=False)
        await message.channel.send(
            embed = embed_message, 
            components = [Button(style=ButtonStyle.green, label='Inscrição', custom_id='subscribe')])

async def subscribe(message, content):
    event = database.find_event(content)
    if event:
        description = f"Interaja aqui para se inscrever na lista de **{content}**"
        embed_message = Embed(title="Inscrição", description=description, color=YELLOW)
        embed_message.add_field(name="Novos inscritos", value="-", inline=False)
        await message.channel.send(
            embed = embed_message,
            components = [Button(style=ButtonStyle.green, label='Inscrição', custom_id='subscribe')])
    else:
        await inexistent_event(message)

async def insert_user(message, name, mention, event):
    if database.find_event(event) == None:
        await inexistent_event(message)
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

async def list_events(message):
    description = LOADING
    embed_message = Embed(title="Eventos cadastrados", value=description, color=YELLOW)
    msg = await message.channel.send(embed=embed_message)
    events = database.find_all_events()
    if len(events) == 0:
        embed_message.description = "- Não há eventos cadastrados -"
        await msg.edit(embed=embed_message)
        return

    await msg.edit(embed=embed_message)
    for event in events:
        if description == LOADING:
            description = f"- {event[1]}\n" + LOADING
        else:
            items = description.split(LOADING)
            description = items[0] + f"- {event[1]}\n" + LOADING

        embed_message.description = description
        await msg.edit(embed=embed_message)
    
    items = description.split(LOADING)
    embed_message.description = items[0]
    await msg.edit(embed=embed_message)

async def list_users(message, content):
    event = database.find_event(content)
    if event == None:
        await inexistent_event(message)
        return

    users = database.find_event_users(content)
    description = LOADING
    embed_message = Embed(title=f"{content}", description=description, color=YELLOW)
    embed_message.add_field(name=f"Criado por: ", value=f"{event[2]}", inline=False)
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

async def call_users(message, content):
    event = database.find_event(content)
    event_name = event[1]
    if event == None:
        await inexistent_event(message)
        return

    users = database.find_event_users(content)
    if len(users) == 0:
        description = "- Não há inscritos -"
        await message.channel.send(
            embed = Embed(title=f"Chamada {content}", description=description, color=YELLOW), 
            delete_after = DELETE_WARN)
        return

    loading_msg = await message.channel.send(LOADING)
    call_msg = f"{event_name}\n{'='*len(event_name)}\n"
    for i, user in enumerate(users, start=1):
        call_msg += f"{i}) {user[2]}\n"
        
    await message.channel.send(call_msg)
    await loading_msg.delete()

async def rename_event(message, content, user_mention):
    separator = '-'
    if separator not in content:
        description = f"Por favor, separe o nome e o novo nome com o caráctere **{separator}** (hífen)"
        await message.channel.send(
            embed = Embed(title="Aviso", description=description, color=RED), 
            delete_after = DELETE_ERROR)
        return
    
    itens = content.split(separator)
    event_name = itens[0].strip()
    new_event_name = itens[1].strip()
    if new_event_name == '':
        description = f"Novo nome de evento inválido."
        await message.channel.send(
            embed = Embed(title="Aviso", description=description, color=RED), 
            delete_after = DELETE_ERROR)
        return
    if database.find_event(event_name) == None:
        await inexistent_event(message)
        return

    result = database.rename_event(user_mention, event_name, new_event_name)
    if result == False:
        description = f"Não foi possível renomear o evento. Não se esqueça" \
            " que apenas o criador do evento possui permissão para renomeá-lo."
        await message.channel.send(
            embed = Embed(title="Aviso", description=description, color=RED), 
            delete_after = DELETE_ERROR)
    else:
        description = f"Evento renomeado com sucesso."
        await message.channel.send(
            embed = Embed(title=f"Renomear evento {config['CHECK']}", description=description, color=GREEN), 
            delete_after = DELETE_WARN)
    
async def remove_subscription(message, content):
    evento = database.find_event(content)
    if evento:
        description = f"Interaja aqui para retirar seu nome da lista de **{content}**"
        embed_message = Embed(title=f"Remover inscrição", description=description, color=YELLOW)
        embed_message.add_field(name="Removidos", value="-", inline=False)
        msg = await message.channel.send(
            embed = embed_message,
            components = [Button(style=ButtonStyle.red, label='Sair', custom_id='exit')])
    else:
        await inexistent_event(message)

async def remove_subscription_reponse(message, name, mention, event):
    if database.find_event(event) == None:
        await inexistent_event(message)
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

async def remove_event(message, content):
    if database.find_event(content) == None:
        await inexistent_event(message)
        return
    
    description = f"{config['WARN']}Atenção{config['WARN']}\nAo confirmar, **{content}** será deletado.\n\n" \
        "**Não se esqueça que apenas quem criou o evento possui permissão para excluí-lo.**"
    await message.channel.send(
        embed = Embed(title="Excluir evento", description=description, color=YELLOW),
        components = [Button(style=ButtonStyle.red, label='Excluir', custom_id='delete')],
        delete_after = DELETE_WARN)

async def remove_event_response(message, user, event):
    result = database.delete_event(event, user)
    if result == False:
        description = "Não foi possível remover o evento"
        await message.channel.send(
            embed = Embed(title="Aviso", description=description, color=RED), 
            delete_after = DELETE_ERROR)
    else:
        description = "Evento removido com sucesso"
        await message.channel.send(
            embed = Embed(title=f"Excluir evento {config['CHECK']}", description=description, color=GREEN), 
            delete_after = DELETE_WARN)

async def select_event_list(message, title, custom_id):
    events = database.find_all_events()
    if len(events) == 0:
        description = "- Não há eventos cadastrados -"
        embed_message = Embed(title=f"Eventos cadastrados", description=description, color=YELLOW)
        await message.channel.send(embed=embed_message, delete_after = DELETE_WARN)
        return

    options = []
    for e in events:
        options.append(
            SelectOption(
                label = e[1][:24],
                value = e[1]
            )
        )
    await message.channel.send(title, delete_after = DELETE_WARN,
        components = [
            Select(
                placeholder = "Selecione o evento",
                options = options,
                custom_id = custom_id
            )
        ]
    )

async def inexistent_event(message):
    description = "Este evento não está cadastrado"
    await message.channel.send(
        embed = Embed(title="Aviso", description=description, color=RED), 
        delete_after = DELETE_ERROR)

async def type_event_name(message):
    description = "Por favor, digite o nome do evento após o comando"
    await message.channel.send(
        embed = Embed(title="Aviso", description=description, color=RED), 
        delete_after = DELETE_ERROR)

async def ping(message):
    pongs = ['tô aqui consagrado', 'diga campeão', 'ô amigo', 'opa', 'Êêê boi', 
        'fala corno', 'diga gay', 'oba', 'tô aqui']
    title = choice(pongs)
    await message.channel.send(
        embed = Embed(title='pong', description=title, color=BLUE), 
        delete_after = DELETE_ERROR)

async def source_link(message):
    description = "O conhecimento serve para ser compartilhado.\n" \
        "O código do Bot de Lista de Chamada é aberto a todos.\n" \
        "Clique no ícone de url para ser redirecionado."
    embed_message = Embed(title="Código do bot", description=description, color=BLUE)
    embed_message.set_footer(
        text="Beijos de tio Crispim", 
        icon_url=config['ICON_URL'])
    await message.channel.send(
        embed = embed_message,
        components = [Button(style=ButtonStyle.URL, label='url', url=config['GITHUB'])])