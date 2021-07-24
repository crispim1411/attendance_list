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

        elif message.content.startswith(config['PREFIX'] + 'source'):
            await send_message.source_link(message)

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
        
