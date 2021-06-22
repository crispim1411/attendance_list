import random
import string

import database
import attendance

event_name = 'event_test'
user_name  = 'user_test'
user_name2 = 'user_test2'
user_name3 = 'user_test3'
user_mention  = '<@user_mention>'
user_mention2 = '<@user_mention2>'
user_mention3 = '<@user_mention3>'

#### DATABASE TESTS ####

def test_find_inexistent_user():
    random_user = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
    users = database.find_user(random_user)
    print(f"\ninexistent user: {users}")
    assert not any([user for user in users if user.name == user_name])

def test_find_inexistent_event():
    random_event = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
    event = database.find_event(random_event)
    print(f"inexistent event: {event}")
    assert event == None

def test_insert_event():
    result = database.insert_event(event_name)
    if result == False:
        print("Evento já existe no banco de dados")
        assert False
    event = database.find_event(event_name)
    print(f"insert event: {event}")
    assert event.name == event_name
    
def test_insert_user():
    result = database.insert_user(user_name, user_mention, event_name)
    if result == False:
        print("Não foi possível cadastrar o usuário")
        assert False
    users = database.find_user(user_name)
    print(f"insert user: {[(i.name, i.mention) for i in users]}")
    assert any([user for user in users if user.name == user_name])

def test_insert_event_users():
    result1 = database.find_user(user_name2)
    result2 = database.find_user(user_name3)
    database.insert_user(user_name2, user_mention2, event_name)
    database.insert_user(user_name3, user_mention3, event_name)
    users = database.find_event_users(event_name)
    if len(users) < 2:
        assert False
    print(f"insert event users: {[(i.name, i.mention) for i in users]}")
    assert users[0].name == user_name
    assert users[1].name == user_name2
    assert users[2].name == user_name3
    assert users[0].mention == user_mention
    assert users[1].mention == user_mention2
    assert users[2].mention == user_mention3

def test_delete_user():
    user = database.find_user(user_name)
    print(f"delete user - before: {[(i.name, i.mention) for i in user]}")
    if user == []:
        assert False
    result = database.delete_user(user_name, event_name)
    assert result != False
    user = database.find_user(user_name)
    print(f"delete user - after: {[(i.name, i.mention) for i in user]}")
    assert user == []

def test_delete_event():
    result = database.insert_event(event_name)
    if result == False:
        print("Evento já existe no banco de dados")
        assert False
    event = database.find_event(event_name)
    print(f"delete event - before: {event}")
    if event == None:
        assert False
    result = database.delete_event(event_name)
    assert result != False
    event = database.find_event(event_name)
    print(f"delete event - after: {event}")
    assert event == None