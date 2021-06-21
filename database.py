from sqlalchemy import create_engine, Column, Integer, String, Sequence, ForeignKey
from sqlalchemy.orm import scoped_session, sessionmaker, relationship, backref
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    name = Column(String, nullable=False)
    event_id = Column(Integer, ForeignKey('events.id'))
    event = relationship('Event', backref=backref('users'))

    def __repr__(self):
        return f"<User(name={self.name!r}, event={self.event.name!r})>"

class Event(Base):
    __tablename__ = 'events'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    def __repr__(self):
        return f"<Event(name={self.name!r})>"

engine = create_engine('sqlite:///:memory:')
session = scoped_session(sessionmaker(bind=engine))
Base.metadata.create_all(engine)

def insert_event(name):
    event = Event(name=name)
    session.add(event)

def insert_user(name, event):
    e = session.query(Event).filter_by(name=event).first()
    user = User(name=name, event=e)
    session.add(user)

def find_all_events():
    return session.query(Event).all()

def find_all_users():
    return session.query(User).all()

def find_event(name):
    return session.query(Event).filter_by(name=name).all()

def find_user(name):
    return session.query(User).filter_by(name=name).all()

def find_event_users(event):
    event = session.query(Event).first()
    return session.query(User).all()

if __name__ == '__main__':
    insert_event('aula de mecanica')
    insert_event('aula de costura')
    insert_user(name='eduard',event='aula de mecanica')
    insert_user(name='marcos',event='aula de costura')
    insert_user(name='lua',event='aula de mecanica')
    insert_user(name='joja',event='aula de mecanica')
    insert_user(name='joja',event='aula de costura')

    print('TODOS OS EVENTOS')
    for e in find_all_events():
        print(e)

    print('\n')
    print('TODOS OS USUARIOS')

    for u in find_all_users():
        print(u)

    print('\n')
    print('TODOS OS USUARIOS DO CURSO DE COSTURA')    

    for u in find_event_users('aula de costura'):
        print(u)

