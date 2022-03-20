from datetime import datetime
import psycopg2
import logging
from config import Config
from urllib.parse import urlparse
from contextlib import contextmanager

# tables
class DBTable:
    event = "events"
    user = "users"


@contextmanager
def open_db():
    try:
        url = urlparse(Config.database_url)
        connection = psycopg2.connect(
            dbname=url.path[1:],
            user=url.username,
            password=url.password,
            host=url.hostname,
            port=url.port)
        cursor = connection.cursor()
        yield cursor
    except Exception as err:
        logging.error(err)
    finally:
        connection.commit()
        connection.close()


def find_event(name, server_id):
    with open_db() as cursor:
        cursor.execute(f"""
            SELECT * FROM {DBTable.event}
            WHERE name ILIKE %s AND server_id = %s
            """, (name, server_id,))
        return cursor.fetchone()


def insert_event(name, creator, server_id):
    event = find_event(name, server_id)
    if event:
        return False

    with open_db() as cursor:
        cursor.execute(f"""
            INSERT INTO {DBTable.event}(name, creator, server_id)
            VALUES (%s, %s, %s)
            """, (name, creator, server_id,))
        return True


def insert_user(name, mention, event_name, server_id):
    event = find_event(event_name, server_id) 
    with open_db() as cursor:
        cursor.execute(f""" 
            SELECT * FROM {DBTable.user}
            WHERE mention = %s AND event_id = %s
            """, (mention, event[0],))

        if cursor.fetchone() == None:
            cursor.execute(f"""
                INSERT INTO {DBTable.user}(name, mention, event_id)
                VALUES (%s, %s, %s)
                """, (name, mention, event[0],))
        else:
            return False


def find_all_events():
    with open_db() as cursor:
        cursor.execute(f"SELECT * FROM {DBTable.event} ORDER BY server_id")
        return cursor.fetchall()


def find_events_in_server(server_id):
    delete_expired_events(server_id)
    with open_db() as cursor:
        cursor.execute(f"""
            SELECT * FROM {DBTable.event} 
            WHERE server_id = %s
            ORDER BY id""", (server_id,))
        return cursor.fetchall()


def find_user(mention):
    with open_db() as cursor:
        cursor.execute(f"""
            SELECT * FROM {DBTable.user}
            WHERE mention = %s
            """, (mention,))
        return cursor.fetchall()


def find_event_users(event_name, server_id):
    with open_db() as cursor:
        cursor.execute(f"""
            SELECT U.* FROM {DBTable.user} U
            INNER JOIN {DBTable.event} E ON E.id = U.event_id
            WHERE E.name ILIKE %s AND E.server_id = %s
            ORDER BY U.id
            """, (event_name, server_id,))
        return cursor.fetchall()


def rename_event(user_mention, event_name, new_name, server_id):
    event = find_event(event_name, server_id) 
    if event[2] != user_mention:
            return False

    with open_db() as cursor:
        cursor.execute(f"""
            UPDATE {DBTable.event} 
            SET name = %s
            WHERE id = %s AND server_id = %s""",
            (new_name, event[0], server_id,))


def delete_event(event_name, user_mention, server_id):
    event = find_event(event_name, server_id) 
    if not event:
        return False
    elif event[2] != user_mention:
        return False

    with open_db() as cursor:
        cursor.execute(f"""
            DELETE FROM {DBTable.user}
            WHERE event_id = %s""", (event[0],))
        cursor.execute(f"""
            DELETE FROM {DBTable.event}
            WHERE id = %s""", (event[0],))


def delete_user(user_mention, event_name, server_id):
    event = find_event(event_name, server_id) 

    with open_db() as cursor:
        cursor.execute(f"""
            SELECT * FROM {DBTable.user}
            WHERE mention = %s AND event_id = %s
            """, (user_mention, event[0],))

        if cursor.fetchone():
            cursor.execute(f"""
                DELETE FROM {DBTable.user}
                WHERE mention = %s AND event_id = %s
                """, (user_mention, event[0],))
        else:
            return False


def count_event_users(event_name, server_id):
    with open_db() as cursor:
        cursor.execute(f"""
            SELECT COUNT(U.id) FROM {DBTable.user} U
            INNER JOIN {DBTable.event} E ON E.id = U.event_id
            WHERE E.name ILIKE %s AND E.server_id = %s
            """, (event_name, server_id,))
        return cursor.fetchone()[0] 

def change_expiration(event_id, server_id, new_exp):
    with open_db() as cursor:
        cursor.execute(f"""
            UPDATE {DBTable.event} 
            SET expiration = %s
            WHERE id = %s AND server_id = %s""",
            (new_exp, event_id, server_id,))
        return True

def delete_expired_events(server_id):
    with open_db() as cursor:
        cursor.execute(f"""
                SELECT * FROM {DBTable.event} 
                WHERE server_id = %s
                ORDER BY id""", (server_id,))
        events = cursor.fetchall()
    
        now = datetime.now()
        for event in events:
            date_created = event[4]
            expiration = event[5]
            diff_month = (now.year - date_created.year)*12 + (now.month - date_created.month)

            if diff_month >= expiration:
                cursor.execute(f"""
                    DELETE FROM {DBTable.user}
                    WHERE event_id = %s""", (event[0],))
                cursor.execute(f"""
                    DELETE FROM {DBTable.event}
                    WHERE id = %s""", (event[0],))