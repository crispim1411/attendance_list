import logging
import src.process_command as process_command
import src.send_message as send_message
from config import Config

from discord.ext import commands
from discord.errors import HTTPException
from discord_components import DiscordComponents
from discord_components.interaction import InteractionType

client = commands.Bot(command_prefix = Config.prefix)


@client.event
async def on_ready():
    DiscordComponents(client)
    logging.info(f"We have logged in as {client.user}")


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith(Config.prefix):
        await process_command.process_data(message)


@client.event
async def on_button_click(interaction):
    user = interaction.author
    mention = f'<@!{user.id}>'
    message = interaction.message
    action = interaction.component.custom_id
    content = interaction.raw_data['d']['message']['embeds'][0]['description']
    current_event = content.split('**')[1]

    try:
        await interaction.respond(type=InteractionType.UpdateMessage)
    except HTTPException as err:
        logging.error(err)
    
    match action:
        case 'subscribe':
            await send_message.insert_user(message, user.name, mention, current_event)
        case 'exit':
            await send_message.remove_subscription_reponse(message, user.name, mention, current_event)
        case 'delete':
            await send_message.remove_event_response(message, mention, current_event)


@client.event
async def on_select_option(interaction):
    item = interaction.component[0].value
    message = interaction.message
    action = interaction.custom_id

    try:
        await interaction.respond(type=InteractionType.UpdateMessage)
        await interaction.message.delete()
    except HTTPException as err:
        logging.error(err)

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


if __name__ == '__main__':
    client.run(Config.token)
