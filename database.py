import os
import psycopg2
from urllib.parse import urlparse

try:
    DATABASE_URL = os.environ['DATABASE_URL']
except:
    from config import DATABASE_URL

url = urlparse(DATABASE_URL)
connection = psycopg2.connect(
    dbname=url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port
    )

def insert_event(name):
    with connection, connection.cursor() as cursor:
        cursor.execute("""
            SELECT * FROM events
            WHERE name LIKE %s
            """, (name))
        if cursor.fetchone():
            return False
        cursor.execute("""
            INSERT INTO events(name)
            VALUES (%s) RETURNING id;
            """, (name))
        event_id = cursor.fetchone()[0]
        return event_id

def insert_user(name, mention, event_name):
    event = find_event(event_name) 
    with connection, connection.cursor() as cursor:
        cursor.execute(""" 
            SELECT U.* FROM users U
            INNER JOIN events E ON E.id = U.event_id
            WHERE E.name LIKE %s AND U.mention = %s
            """, (name, mention))
        if cursor.fetchone() == None:
            cursor.execute("""
                INSERT INTO users(name, mention, event_id)
                VALUES (%s, %s, %s) RETURNING id;
                """, (name, mention, event[0]))
        else:
            return False

def find_all_events():
    with connection, connection.cursor() as cursor:
        cursor.execute("SELECT * FROM events")
        events = cursor.fetchall()
        return events

def find_all_users():
    ...

def find_event(name):
    with connection, connection.cursor() as cursor:
        cursor.execute("""
            SELECT * FROM events
            WHERE name LIKE %s
            """, (name,))
        event = cursor.fetchone()
        return event

def find_user(name):
    ...

def find_event_users(event_name):
    with connection, connection.cursor() as cursor:
        cursor.execute("""
            SELECT U.* FROM users U
            INNER JOIN events E ON E.id = U.event_id
            WHERE E.name LIKE %s
            """, (event_name,))
        users = cursor.fetchall()
        return users

def delete_event(event_name):
    ...

def delete_user(user_mention, event_name):
    ...


