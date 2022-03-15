import psycopg2
import logging
from urllib.parse import urlparse
from config import Config

def connect():
    try:
        url = urlparse(Config.database_url)
        connection = psycopg2.connect(
            dbname=url.path[1:],
            user=url.username,
            password=url.password,
            host=url.hostname,
            port=url.port
            )
        return connection
    except Exception as e:
        logging.error(f"Error while establishing database connection: {e}")
    
def connect_to_database(func):
    def wrapper(*args, **kwargs):
        connection = connect()
        args += (connection,)
        return func(*args, *kwargs)
    return wrapper


@connect_to_database
def insert_event(name, creator, server_id, connection=None):
    event = find_event(name, server_id)
    if event:
        return False
    try:
        with connection, connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO events(name, creator, server_id)
                VALUES (%s, %s, %s)
                """, (name, creator, server_id,))
            return True
    finally:
        connection.close()

@connect_to_database
def insert_user(name, mention, event_name, server_id, connection=None):
    event = find_event(event_name, server_id) 
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
            cursor.execute("SELECT * FROM events ORDER BY server_id")
            return cursor.fetchall()
    finally:
        connection.close()

@connect_to_database
def find_events_in_server(server_id, connection=None):
    try:
        with connection, connection.cursor() as cursor:
            cursor.execute("""
                SELECT * FROM events 
                WHERE server_id = %s
                ORDER BY id""", (server_id,))
            return cursor.fetchall()
    finally:
        connection.close()

@connect_to_database
def find_event(name, server_id, connection):
    try:
        with connection, connection.cursor() as cursor:
            cursor.execute("""
                SELECT * FROM events
                WHERE name ILIKE %s AND server_id = %s
                """, (name, server_id,))
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
def find_event_users(event_name, server_id, connection=None):
    try:
        with connection, connection.cursor() as cursor:
            cursor.execute("""
                SELECT U.* FROM users U
                INNER JOIN events E ON E.id = U.event_id
                WHERE E.name ILIKE %s AND E.server_id = %s
                ORDER BY U.id
                """, (event_name, server_id,))
            return cursor.fetchall()
    finally:
        connection.close()

@connect_to_database
def rename_event(user_mention, event_name, new_name, server_id, connection=None):
    event = find_event(event_name, server_id) 
    try:
        with connection, connection.cursor() as cursor:
            if event[2] != user_mention:
                return False
            cursor.execute("""
                UPDATE events 
                SET name = %s
                WHERE id = %s AND server_id = %s""",
                (new_name, event[0], server_id,))
    finally:
        connection.close()

@connect_to_database
def delete_event(event_name, user_mention, server_id, connection=None):
    event = find_event(event_name, server_id) 
    if not event:
        return False
    elif event[2] != user_mention:
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
def delete_user(user_mention, event_name, server_id, connection=None):
    event = find_event(event_name, server_id) 
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
    
@connect_to_database
def count_event_users(event_name, server_id, connection=None):
    try:
        with connection, connection.cursor() as cursor:
            cursor.execute("""
                SELECT COUNT(U.id) FROM users U
                INNER JOIN events E ON E.id = U.event_id
                WHERE E.name ILIKE %s AND E.server_id = %s
                """, (event_name, server_id,))
            return cursor.fetchone()[0] 
    finally:
        connection.close()