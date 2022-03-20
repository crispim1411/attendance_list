import logging
from src.models import ClickMessage, SelectMessage
import src.process_command as process_command
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
    action = interaction.component.custom_id
    click_msg = ClickMessage(
        user = interaction.author,
        message = interaction.message,
        event = interaction.raw_data['d']['message']['embeds'][0]['description'].split('**')[1])

    try:
        await interaction.respond(type=InteractionType.UpdateMessage)
        await process_command.process_click_button(action, click_msg)
    except HTTPException as err:
        logging.error(err)


@client.event
async def on_select_option(interaction):
    action = interaction.custom_id
    select_msg = SelectMessage(
        message = interaction.message,
        content = interaction.component[0].value)

    try:
        await interaction.respond(type=InteractionType.UpdateMessage)
        await interaction.message.delete()
        await process_command.process_select_list(action, select_msg)
    except HTTPException as err:
        logging.error(err)


if __name__ == '__main__':
    logging.basicConfig(level=logging.ERROR)
    client.run(Config.token)
