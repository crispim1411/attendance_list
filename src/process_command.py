from config import Config
from src import send_message

funcs_1_param = {
    'help': send_message.help,
    'eventos': send_message.list_events,
    'inscrever': send_message.select_subscribe_list,
    'chamada': send_message.select_call_list,
    'info': send_message.select_info_list,
    'sair': send_message.select_exit_list,
    'excluir': send_message.select_delete_list,
    'renomear': send_message.type_event_name,
    'criar': send_message.type_event_name,
    'source': send_message.source_link,
    'ping': send_message.ping
}

funcs_2_param = {
    'inscrever': send_message.subscribe,
    'chamada': send_message.call_users,
    'info': send_message.list_users,
    'sair': send_message.remove_subscription,
    'excluir': send_message.remove_event,
    'renomear': send_message.rename_event,
    'criar': send_message.new_event
}

async def process_data(message):
    content = message.content.lstrip(Config.prefix)
    itens = content.split(' ')
    
    if content == 'eventos -a':
        return await send_message.list_all_events(message)

    command = itens[0]
    
    if len(itens) == 1:
        func = funcs_1_param.get(command)
        if func:
            await func(message)    
    else:
        func = funcs_2_param.get(command)
        if func:
            await func(message, content)  


async def process_click_button(click_msg):
    message = click_msg.message
    mention = click_msg.mention
    current_event = click_msg.current_event
    user = click_msg.user
    action = click_msg.action

    match action:
        case 'subscribe':
            await send_message.insert_user(message, user.name, mention, current_event)
        case 'exit':
            await send_message.remove_subscription_reponse(message, user.name, mention, current_event)
        case 'delete':
            await send_message.remove_event_response(message, mention, current_event)


async def process_select_list(select_msg):
    message = select_msg.message
    item = select_msg.item
    action = select_msg.action

    match action:
        case 'subscribe_select': 
            await send_message.subscribe(message, item)
        case 'call_select':
            await send_message.call_users(message, item)
        case 'info_select':
            await send_message.list_users(message, item)
        case 'exit_select':
            await send_message.remove_subscription(message, item)
        case 'delete_select':
            await send_message.remove_event(message, item)