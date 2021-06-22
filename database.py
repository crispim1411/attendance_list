from sqlalchemy import create_engine, Column, Integer, String, Sequence, ForeignKey
from sqlalchemy.orm import scoped_session, sessionmaker, relationship, backref
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    name = Column(String, nullable=False)
    mention = Column(String, nullable=False)
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
    with Session.begin() as session:
        if session.query(Event).filter_by(name=name).count() == 0:
            event = Event(name=name)
            session.add(event)
        else:
            return False

def insert_user(name, mention, event_name):
    with Session.begin() as session:
        event = session.query(Event).filter_by(name=event_name).first()
        if event:
            if session.query(User).filter_by(name=name, event=event).count() == 0:
                user = User(name=name, mention=mention, event=event)
                session.add(user)
            else:
                return False
        else:
            return False

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
        event = session.query(Event).filter_by(name=name).first()
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

def delete_event(event_name):
    with Session.begin() as session:
        event = session.query(Event).filter_by(name=event_name).first()
        if event:
            users = session.query(User).filter_by(event=event).delete()
            session.delete(event)
        else:
            return False

def delete_user(user_mention, event_name):
    with Session.begin() as session:
        event = session.query(Event).filter_by(name=event_name).first()
        if event:
            user = session.query(User).filter_by(mention=user_mention, event=event).first()
            if not user:
                return False
            session.delete(user)
        else:
            return False

        

