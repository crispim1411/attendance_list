# imports do projeto
import send_message
from config import config

async def process_data(message):
    itens = message.content.split(' ')
    
    if message.content == config['PREFIX'] or message.content == config['PREFIX'] + 'help':
        await send_message.help(message)
        return

    if len(itens) == 1:
        if message.content == config['PREFIX'] + 'eventos':
            await send_message.list_events(message)

        elif message.content == config['PREFIX'] + 'inscrever':
            await send_message.select_event_list(message, 'Inscrição', 'subscribe_select')

        elif message.content == config['PREFIX'] + 'chamada':
            await send_message.select_event_list(message, 'Chamada', 'call_select')

        elif message.content == config['PREFIX'] + 'info':
            await send_message.select_event_list(message, 'Info', 'info_select')

        elif message.content == config['PREFIX'] + 'sair':
            await send_message.select_event_list(message, 'Remover inscrição', 'exit_select')

        elif message.content == config['PREFIX'] + 'excluir':
            await send_message.type_event_name(message)

        elif message.content == config['PREFIX'] + 'renomear':
            await send_message.type_event_name(message)

        elif message.content == config['PREFIX'] + 'source':
            await send_message.source_link(message)

        elif message.content == config['PREFIX'] + 'ping':
            await send_message.ping(message)
        
    else:
        content = ' '.join(itens[1:])

        if message.content.startswith(config['PREFIX'] + 'criar '):
            await send_message.new_event(message, content)

        elif message.content.startswith(config['PREFIX'] + 'inscrever '):
            await send_message.subscribe(message, content)

        elif message.content.startswith(config['PREFIX'] + 'chamada '):
            await send_message.call_users(message, content)

        elif message.content.startswith(config['PREFIX'] + 'info '):
            await send_message.list_users(message, content)

        elif message.content.startswith(config['PREFIX'] + 'sair '):
            await send_message.remove_subscription(message, content)

        elif message.content.startswith(config['PREFIX'] + 'excluir '):
            await send_message.remove_event(message, content)

        elif message.content.startswith(config['PREFIX'] + 'renomear' ):
            await send_message.rename_event(message, content, message.author.mention)
        
        elif message.content == config['PREFIX'] + 'eventos -a':
            await send_message.list_all_events(message)
        
