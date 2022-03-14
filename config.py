from dataclasses import dataclass

@dataclass
class Config:
    prefix = "*"
    check = '\U00002705'
    cross = '\U0000274c'
    warn = '\U000026A0'
    github_link = 'https://github.com/crispim1411/attendance_list'
    icon_url = 'https://static.wikia.nocookie.net/digimon-adventure5140/images/f/fd/Digivice_tri.png/revision/latest?cb=20170328025147'

    @classmethod
    @property
    def token(cls): 
        try:
            import credentials
            return credentials.TOKEN
        except:
            import os
            return os.environ['TOKEN']

    @classmethod
    @property
    def database_url(cls): 
        try:
            import credentials
            return credentials.DATABASE_URL
        except:
            import os
            return os.environ['DATABASE_URL']

    @classmethod
    @property
    def root(cls):
        try:
            import credentials
            return credentials.ROOT
        except:
            import os
            return os.environ['ROOT']
