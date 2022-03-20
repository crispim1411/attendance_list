from config import Config
from src import send_message

funcs_click = {
    'subscribe': send_message.subscribe_user_response,
    'exit': send_message.remove_subscription_reponse,
    'delete': send_message.remove_event_response
}

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

# também select list
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
    content = content.lstrip(f"{command} ")
    
    if len(itens) == 1:
        func = funcs_1_param.get(command)
        if func:
            await func(message)    
    else:
        func = funcs_2_param.get(command)
        if func:
            await func(message, content)  


async def process_click_button(action, click_msg):
    func = funcs_click.get(action)
    if func:
        await func(click_msg)    


async def process_select_list(action, select_msg):
    message = select_msg.message
    content = select_msg.content

    func = funcs_2_param.get(action)
    if func:
        await func(message, content)  