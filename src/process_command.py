from config import Config
from src import send_message

async def process_data(message):
    content = message.content.lstrip(Config.prefix)
    itens = content.split(' ')
    
    if content == 'help':
        return await send_message.help(message)

    command = itens[0]

    if len(itens) == 1:
        match command:
            case 'eventos':
                await send_message.list_events(message)
            case 'inscrever':
                await send_message.select_event_list(message, 'Inscrição', 'subscribe_select')
            case 'chamada':
                await send_message.select_event_list(message, 'Chamada', 'call_select')
            case 'info':
                await send_message.select_event_list(message, 'Info', 'info_select')
            case 'sair':
                await send_message.select_event_list(message, 'Remover inscrição', 'exit_select')
            case 'excluir':
                await send_message.select_event_list(message, 'Excluir evento', 'delete_select')
            case 'renomear':
                await send_message.type_event_name(message)
            case 'criar':
                await send_message.type_event_name(message)
            case 'source':
                await send_message.source_link(message)
            case 'ping':
                await send_message.ping(message)
        
    else:
        match command:
            case 'inscrever':
                await send_message.subscribe(message, content)
            case 'chamada':
                send_message.call_users(message, content)
            case 'info':
                await send_message.list_users(message, content)
            case 'sair':
                 await send_message.remove_subscription(message, content)
            case 'excluir':
                await send_message.remove_event(message, content)
            case 'renomear':
                await send_message.rename_event(message, content, message.author.mention)
            case 'criar':
                await send_message.new_event(message, content)
            case 'eventosall':
                await send_message.list_all_events(message)