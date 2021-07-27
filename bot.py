from discord.ext import commands
from discord_components import DiscordComponents
from discord_components.interaction import InteractionType

# imports do projeto 
import process_command
import send_message
from config import config
try:
    import credentials
    TOKEN = credentials.TOKEN
except:
    import os
    TOKEN = os.environ['TOKEN']

client = commands.Bot(command_prefix = config['PREFIX'])
            
@client.event
async def on_ready():
    DiscordComponents(client)
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith(config['PREFIX']):
        await process_command.process_data(message)

@client.event
async def on_reaction_add(reaction, user):
    BOT = client.user.discriminator
    if reaction.message.author.discriminator != BOT \
        or user.discriminator == BOT:
        return

    if len(reaction.message.embeds) == 1:
        embed_description = reaction.message.embeds[0].description
        itens = embed_description.split('**')
    else:
        return

    message = reaction.message
    str_reaction = str(reaction).encode('unicode-escape')
    if len(itens) > 1:
        current_event = itens[1]

        if str_reaction == config['CROSS'].encode('unicode-escape'):
            if message.embeds[0].title == "Excluir evento":
                await send_message.remove_event_response(message, user.mention, current_event)
            else:
                await send_message.remove_subscription_reponse(message, user.name, user.mention, current_event)

@client.event
async def on_button_click(interaction):
    user = interaction.author
    mention = f'<@!{user.id}>'
    message = interaction.message
    action = interaction.component.custom_id
    content = interaction.raw_data['d']['message']['embeds'][0]['description']
    current_event = content.split('**')[1]

    await interaction.respond(type=InteractionType.UpdateMessage)
    
    if action == 'subscribe':
        await send_message.insert_user(message, user.name, mention, current_event)

    elif action == 'exit':
        await send_message.remove_subscription_reponse(message, user.name, mention, current_event)

    elif action == 'delete':
        await send_message.remove_event_response(message, mention, current_event)

@client.event
async def on_select_option(interaction):
    item = interaction.component[0].value
    message = interaction.message
    action = interaction.custom_id

    await interaction.respond(type=InteractionType.UpdateMessage)
    await interaction.message.delete()

    if action == 'subscribe_select': 
        await send_message.subscribe(message, item)
    elif action == 'call_select':
        await send_message.call_users(message, item)
    elif action == 'info_select':
        await send_message.list_users(message, item)
    elif action == 'exit_select':
        await send_message.remove_subscription(message, item)

client.run(TOKEN)
