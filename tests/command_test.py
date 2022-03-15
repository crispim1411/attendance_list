from attr import dataclass
from src import components, process_command

pytest_plugins = ('pytest_asyncio',)

class Channel:
    async def send(self, embed, delete_after=None):
        self.result = embed

@dataclass
class Message:
    channel: Channel
    content: str
    result: str


async def test_help():
    message = Message(channel=Channel(), content="help", result=None)
    await process_command.process_data(message)
    assert message.channel.result == components.help


async def test_event_list():
    message = Message(channel=Channel(), content="eventos", result=None)
    message.guild = lambda: None
    message.guild.id = '0'
    await process_command.process_data(message)
    assert message.channel.result == components.no_events


async def test_select_subscribe():
    message = Message(channel=Channel(), content="inscrever", result=None)
    message.guild = lambda: None
    await process_command.process_data(message)
    assert message.channel.result == components.no_events


# funcs_1_param = {
#     'help': send_message.help,
#     'eventos': send_message.list_events,
#     'inscrever': send_message.select_subscribe_list,
#     'chamada': send_message.select_call_list,
#     'info': send_message.select_info_list,
#     'sair': send_message.select_exit_list,
#     'excluir': send_message.select_delete_list,
#     'renomear': send_message.type_event_name,
#     'criar': send_message.type_event_name,
#     'source': send_message.source_link,
#     'ping': send_message.ping
# }

# funcs_2_param = {
#     'inscrever': send_message.subscribe,
#     'chamada': send_message.call_users,
#     'info': send_message.list_users,
#     'sair': send_message.remove_subscription,
#     'excluir': send_message.remove_event,
#     'renomear': send_message.rename_event,
#     'criar': send_message.new_event
# }