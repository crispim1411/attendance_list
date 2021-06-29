import os
import psycopg2
from urllib.parse import urlparse

try:
    DATABASE_URL = os.environ['DATABASE_URL']
except:
    from config import DATABASE_URL

def connect():
    try:
        url = urlparse(DATABASE_URL)
        connection = psycopg2.connect(
            dbname=url.path[1:],
            user=url.username,
            password=url.password,
            host=url.hostname,
            port=url.port
            )
        return connection
    except Exception as e:
        print(f"Error while establishing database connection: {e}")
    
def connect_to_database(func):
    def wrapper(*args, **kwargs):
        connection = connect()
        args += (connection,)
        return func(*args, *kwargs)
    return wrapper


@connect_to_database
def insert_event(name, connection=None):
    event = find_event(name)
    if event:
        return False

    try:
        with connection, connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO events(name)
                VALUES (%s)
                """, (name,))
            return True
    finally:
        connection.close()

@connect_to_database
def insert_user(name, mention, event_name, connection=None):
    event = find_event(event_name) 
    try:
        with connection, connection.cursor() as cursor:
            cursor.execute(""" 
                SELECT * FROM users
                WHERE mention = %s AND event_id = %s
                """, (mention, event[0],))

            if cursor.fetchone() == None:
                cursor.execute("""
                    INSERT INTO users(name, mention, event_id)
                    VALUES (%s, %s, %s)
                    """, (name, mention, event[0],))
            else:
                return False
    finally:
        connection.close()

@connect_to_database
def find_all_events(connection=None):
    try:
        with connection, connection.cursor() as cursor:
            cursor.execute("SELECT * FROM events")
            return cursor.fetchall()
    finally:
        connection.close()

@connect_to_database
def find_event(name, connection):
    try:
        with connection, connection.cursor() as cursor:
            cursor.execute("""
                SELECT * FROM events
                WHERE name LIKE %s
                """, (name,))
            return cursor.fetchone()
    finally:
        connection.close()

@connect_to_database
def find_user(mention, connection=None):
    try:
        with connection, connection.cursor() as cursor:
            cursor.execute("""
                SELECT * FROM users
                WHERE mention = %s
                """, (mention,))
            return cursor.fetchall()
    finally:
        connection.close()

@connect_to_database
def find_event_users(event_name, connection=None):
    try:
        with connection, connection.cursor() as cursor:
            cursor.execute("""
                SELECT U.* FROM users U
                INNER JOIN events E ON E.id = U.event_id
                WHERE E.name LIKE %s
                """, (event_name,))
            return cursor.fetchall()
    finally:
        connection.close()

@connect_to_database
def delete_event(event_name, connection=None):
    event = find_event(event_name) 
    if not event:
        return False
    try:
        with connection, connection.cursor() as cursor:
            cursor.execute("""
                DELETE FROM users
                WHERE event_id = %s""", (event[0],))
            cursor.execute("""
                DELETE FROM events
                WHERE id = %s""", (event[0],))
    finally:
        connection.close()

@connect_to_database
def delete_user(user_mention, event_name, connection=None):
    event = find_event(event_name) 
    try:
        with connection, connection.cursor() as cursor:
            cursor.execute("""
                SELECT * FROM users
                WHERE mention = %s AND event_id = %s
                """, (user_mention, event[0],))

            if cursor.fetchone():
                cursor.execute("""
                    DELETE FROM users
                    WHERE mention = %s AND event_id = %s
                    """, (user_mention, event[0],))
            else:
                return False
    finally:
        connection.close()
    
