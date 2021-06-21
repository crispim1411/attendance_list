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

engine = create_engine('sqlite:///info.db')
Session = sessionmaker(bind=engine)
Base.metadata.create_all(engine)

def insert_event(name):
    event = Event(name=name)
    with Session.begin() as session:
        session.add(event)

def insert_user(name, event):
    with Session.begin() as session:
        e = session.query(Event).filter_by(name=event).first()
        user = User(name=name, event=e)
        session.add(user, _warn=True)

def find_all_events():
    with Session.begin() as session:
        events = session.query(Event).all()
        session.expunge_all()
        return events

def find_all_users():
    with Session.begin() as session:
        users = session.query(User).all()
        session.expunge_all()
        return users

def find_event(name):
    with Session.begin() as session:
        event = session.query(Event).filter_by(name=name).all()
        session.expunge_all()
        return event

def find_user(name):
    with Session.begin() as session:
        user = session.query(User).filter_by(name=name).all()
        session.expunge_all()
        return user

def find_event_users(event_name):
    with Session.begin() as session:
        event = session.query(Event).filter_by(name=event_name).first()
        users = session.query(User).filter_by(event=event).all()
        session.expunge_all()
        return users

