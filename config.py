try:
    import credentials
    TOKEN = credentials.TOKEN
except:
    import os
    TOKEN = os.environ['TOKEN']

config = {
    'PREFIX': "*",
    'CHECK': '\U00002705',
    'CROSS': '\U0000274c',
    'WARN': '\U000026A0',
    'GITHUB': 'https://github.com/crispim1411/attendance_list',
    'ICON_URL': 'https://static.wikia.nocookie.net/digimon-adventure5140/images/f/fd/Digivice_tri.png/revision/latest?cb=20170328025147',
    'TOKEN': TOKEN
}