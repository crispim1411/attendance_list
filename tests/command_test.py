from attr import dataclass
from src import components, process_command

pytest_plugins = ('pytest_asyncio',)

class ChannelMock:
    async def send(self, embed, delete_after=None, components=[]):
        self.result = embed

@dataclass
class MessageMock:
    channel: ChannelMock
    content: str
    result: str

async def test_help():
    message = MessageMock(channel=ChannelMock(), content="help", result=None)
    await process_command.process_data(message)
    assert message.channel.result == components.help

### 
# Para esses testes é informado server_id 0 por isso é esperado 
# mensagem de No events
 
async def test_event_list_error():
    message = MessageMock(channel=ChannelMock(), content="eventos", result=None)
    message.guild = lambda: None
    message.guild.id = '0'
    await process_command.process_data(message)
    assert message.channel.result == components.no_events

async def test_select_subscribe_error():
    message = MessageMock(channel=ChannelMock(), content="inscrever", result=None)
    message.guild = lambda: None
    message.guild.id = '0'
    await process_command.process_data(message)
    assert message.channel.result == components.no_events

async def test_select_call_error():
    message = MessageMock(channel=ChannelMock(), content="chamada", result=None)
    message.guild = lambda: None
    message.guild.id = '0'
    await process_command.process_data(message)
    assert message.channel.result == components.no_events

async def test_select_info_error():
    message = MessageMock(channel=ChannelMock(), content="info", result=None)
    message.guild = lambda: None
    message.guild.id = '0'
    await process_command.process_data(message)
    assert message.channel.result == components.no_events

async def test_select_exit_error():
    message = MessageMock(channel=ChannelMock(), content="sair", result=None)
    message.guild = lambda: None
    message.guild.id = '0'
    await process_command.process_data(message)
    assert message.channel.result == components.no_events

async def test_select_delete_error():
    message = MessageMock(channel=ChannelMock(), content="excluir", result=None)
    message.guild = lambda: None
    message.guild.id = '0'
    await process_command.process_data(message)
    assert message.channel.result == components.no_events

### 

async def test_rename_error():
    message = MessageMock(channel=ChannelMock(), content="renomear", result=None)
    await process_command.process_data(message)
    assert message.channel.result == components.event_not_typed_error

async def test_create_error():
    message = MessageMock(channel=ChannelMock(), content="criar", result=None)
    await process_command.process_data(message)
    assert message.channel.result == components.event_not_typed_error

async def test_source():
    message = MessageMock(channel=ChannelMock(), content="source", result=None)
    await process_command.process_data(message)
    assert message.channel.result == components.source
