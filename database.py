import os
import psycopg2
from urllib.parse import urlparse

class Database:
    def __init__(self):
        url = urlparse(os.environ['DATABASE_URL'])
        self.connection = connection = psycopg2.connect(
            dbname=url.path[1:],
            user=url.username,
            password=url.password,
            host=url.hostname,
            port=url.port
            )

    def close(self):
        self.connection.close()

def find_all_events():
    con = Database().connection
    cursor = con.cursor()
    cursor.execute("SELECT * FROM events")
    events = cursor.fetchall()
    con.close()
    return events

def insert_event(name):
    con = Database().connection
    cursor = con.cursor()
    command = """INSERT INTO events(name)
             VALUES(%s) RETURNING id;"""
    cursor.execute(command, (name,))
    event_id = cursor.fetchone()[0]
    con.commit()
    con.close()
    return event_id
