from discord_components.component import Select, SelectOption
from discord_components import Button, ButtonStyle
from src import database, components
from config import Config

# Tempo auto delete
DELETE_ERROR = 30
DELETE_WARN  = 60
# Mensagens
LOADING = "carregando..."

### one param methods ###

async def help(message):
    await message.channel.send(embed=components.help)

async def type_event_name(message):
    await message.channel.send(
        embed = components.event_not_typed_error, 
        delete_after = DELETE_ERROR)

async def ping(message):
    await message.channel.send(
        embed = components.ping(), 
        delete_after = DELETE_WARN)

async def source_link(message):
    await message.channel.send(
        embed = components.source,
        components = [Button(style=ButtonStyle.URL, label='url', url=Config.github_link)])

async def select_subscribe_list(message):
    await select_event_list(message, 'Inscrição', 'inscrever')

async def select_call_list(message):
    await select_event_list(message, 'Chamada', 'chamada')

async def select_info_list(message):
    await select_event_list(message, 'Info', 'info')

async def select_exit_list(message):
    await select_event_list(message, 'Remover inscrição', 'sair')

async def select_delete_list(message):
    await select_event_list(message, 'Excluir evento', 'excluir')

async def select_event_list(message, title, custom_id):
    events = database.find_events_in_server(str(message.guild.id))
    if len(events) == 0:
        return await message.channel.send(
            embed = components.no_events, 
            delete_after = DELETE_WARN)

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

async def list_all_events(message):
    # Comando para listar título de todos os eventos de todos os servidores
    # Uso para fins de desenvolvimento, não é possível checar os usuários inscritos
    # apenas os títulos dos eventos
    if message.author.discriminator != Config.root:
        await message.channel.send(
            embed = components.list_root,
            delete_after = DELETE_ERROR)
        return
    
    loading_msg = await message.channel.send(LOADING)
    events = database.find_all_events()
    if len(events) == 0:
        return await message.channel.send(embed=components.no_events)

    server = events[0][3]
    counter = 1
    description = f"--- Server {counter} ---\n"    
    for event in events:
        if event[3] != server:
            server = event[3]
            counter += 1
            description += f"\n--- Server {counter} ---\n"
        description += f"- {event[1]}\n"

    await message.channel.send(embed=components.list_events(description))
    await loading_msg.delete()


async def list_events(message):
    events = database.find_events_in_server(str(message.guild.id))
    if len(events) == 0:
        return await message.channel.send(embed=components.no_events)

    description = ""
    loading_msg = await message.channel.send(LOADING)
    for event in events:
        description += f"- {event[1]}\n"

    await message.channel.send(embed=components.list_events(description))
    await loading_msg.delete()

### two params methods ###

async def new_event(message, content):
    result = database.insert_event(content, message.author.mention, str(message.guild.id))
    if result == False:
        await message.channel.send(
            embed = components.event_already_subscribed, 
            delete_after = DELETE_ERROR)
    else:
        await message.channel.send(
            embed = components.subscribe_event(content), 
            components = [
                Button(
                    style=ButtonStyle.green, 
                    label='Inscrição', 
                    custom_id='subscribe')
            ])

async def subscribe(message, content):
    event = database.find_event(content, str(message.guild.id))
    if event:
        await message.channel.send(
            embed = components.subscribe_event(content),
            components = [
                Button(
                    style=ButtonStyle.green, 
                    label='Inscrição', 
                    custom_id='subscribe')
            ])
    else:
        await message.channel.send(
            embed = components.no_events, 
            delete_after = DELETE_ERROR)

async def list_users(message, content):
    server_id = str(message.guild.id)
    event = database.find_event(content, server_id)
    if event == None:
        return await message.channel.send(
            embed = components.no_events, 
            delete_after = DELETE_ERROR)

    users = database.find_event_users(content, server_id)
    if len(users) == 0:
        return await message.channel.send(embed=components.no_subscribers(content))

    description = ""
    loading_msg = await message.channel.send(LOADING)
    for i, user in enumerate(users, start=1):
        description += f"{i}) {user[1]}\n"
    
    await message.channel.send(embed=components.list_event_users(content, description, event[2]))
    await loading_msg.delete()

async def call_users(message, content):
    server_id = str(message.guild.id)
    event = database.find_event(content, server_id)
    event_name = event[1]
    if event == None:
        return await message.channel.send(
            embed = components.no_events, 
            delete_after = DELETE_ERROR)

    users = database.find_event_users(content, server_id)
    if len(users) == 0:
        return await message.channel.send(embed=components.no_subscribers(content))

    loading_msg = await message.channel.send(LOADING)
    call_msg = f"{event_name}\n{'='*len(event_name)}\n"
    for i, user in enumerate(users, start=1):
        call_msg += f"{i}) {user[2]}\n"
        
    await message.channel.send(call_msg)
    await loading_msg.delete()

async def rename_event(message, content):
    separator = '-'
    if separator not in content:
        return await message.channel.send(
            embed = components.no_separator, 
            delete_after = DELETE_ERROR)
        
    itens = content.split(separator)
    event_name = itens[0].strip()
    new_event_name = itens[1].strip()
    if new_event_name == '':
        return await message.channel.send(
            embed = components.event_invalid_name, 
            delete_after = DELETE_ERROR)
        
    server_id = str(message.guild.id)
    if database.find_event(event_name, server_id) == None:
        return await message.channel.send(
            embed = components.no_events, 
            delete_after = DELETE_ERROR)

    user_mention = message.author.mention
    result = database.rename_event(user_mention, event_name, new_event_name, server_id)
    if result == False:
        await message.channel.send(
            embed = components.rename_perm_error, 
            delete_after = DELETE_ERROR)
    else:
        await message.channel.send(
            embed = components.rename_success, 
            delete_after = DELETE_WARN)

async def remove_subscription(message, content):
    evento = database.find_event(content, str(message.guild.id))
    if evento:
        await message.channel.send(
            embed = components.remove_subscription(content),
            components = [Button(style=ButtonStyle.red, label='Sair', custom_id='exit')])
    else:
        await message.channel.send(
            embed = components.no_events, 
            delete_after = DELETE_ERROR)

async def remove_event(message, content):
    if database.find_event(content, str(message.guild.id)) == None:
        return await message.channel.send(
            embed = components.no_events, 
            delete_after = DELETE_ERROR)
    
    await message.channel.send(
        embed = components.remove_event(content),
        components = [Button(style=ButtonStyle.red, label='Excluir', custom_id='delete')],
        delete_after = DELETE_WARN)

### Click methods ###

async def subscribe_user_response(click_msg):
    message = click_msg.message
    user = click_msg.user
    mention = click_msg.mention
    event = click_msg.mention.event
    
    server_id = str(message.guild.id)
    if database.find_event(event, server_id) == None:
        return await message.channel.send(
            embed = components.no_events, 
            delete_after = DELETE_ERROR)
        
    result = database.insert_user(user, mention, event, server_id)
    if result == False:
        await message.channel.send(
            embed = components.already_subscribed(user, event), 
            delete_after = DELETE_ERROR)
    else:
        await message.edit(
            embed=components.update_subscription_msg(message.embeds[0], user))

async def remove_subscription_reponse(click_msg):
    message = click_msg.message
    user = click_msg.user
    mention = click_msg.mention
    event = click_msg.mention.event

    server_id = str(message.guild.id)
    if database.find_event(event, server_id) == None:
        return await message.channel.send(
            embed = components.no_events, 
            delete_after = DELETE_ERROR)

    result = database.delete_user(mention, event, server_id)
    if result == False:
        await message.channel.send(
            embed = components.not_subscribed(event, user),
            delete_after = DELETE_ERROR)
    else:
        await message.channel.send(
            embed=components.unsubscribed(event, user),
            delete_after = DELETE_ERROR)

async def remove_event_response(click_msg):
    message = click_msg.message
    mention = click_msg.mention
    event = click_msg.mention.event

    result = database.delete_event(event, mention, str(message.guild.id))
    if result == False:
        await message.channel.send(
            embed = components.remove_event_error, 
            delete_after = DELETE_ERROR)
    else:
        await message.channel.send(
            embed = components.remove_event_success, 
            delete_after = DELETE_WARN)