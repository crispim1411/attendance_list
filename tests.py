import random
import string
# import do projeto
import database

event_name = 'event_test'
event_name2 = 'event_test2'
user_name  = 'user_test'
user_name2 = 'user_test2'
user_name3 = 'user_test3'
user_mention  = '<@user_mention>'
user_mention2 = '<@user_mention2>'
user_mention3 = '<@user_mention3>'

#### DATABASE TESTS ####

def test_find_inexistent_user():
    random_mention = '<@' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=10)) + '>'
    users = database.find_user(random_mention)
    assert not any([user for user in users if user[1] == user_name])

def test_find_inexistent_event():
    random_event = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
    event = database.find_event(random_event)
    assert event == None

def test_insert_event():
    # tenta criar evento 1
    result = database.insert_event(event_name, user_mention)
    assert result != False
    # checa se evento foi criado
    event = database.find_event(event_name)
    assert event[1] == event_name
    # Checando unicidade da inserção
    result = database.insert_event(event_name, user_mention)
    assert result == False

    #repete para event_name2
    result2 = database.insert_event(event_name2, user_mention)
    assert result2 != False
    event2 = database.find_event(event_name2)
    assert event2[1] == event_name2
    result2 = database.insert_event(event_name2, user_mention)
    assert result2 == False
    
def test_insert_user():
    # checa se o usuario não existe no evento
    users = database.find_event_users(event_name)
    assert not any([user for user in users if user[1] == user_name])
    # insere o usuario
    result = database.insert_user(user_name, user_mention, event_name)
    assert result != False
    # checa se o usuário foi inserido
    users = database.find_event_users(event_name)
    assert any([user for user in users if user[1] == user_name])
    # checando unicidade da inserção
    result = database.insert_user(user_name, user_mention, event_name)
    assert result == False
    
    # repete para user_name2 -> event_name
    users = database.find_event_users(event_name)
    assert not any([user for user in users if user[1] == user_name2])
    result = database.insert_user(user_name2, user_mention2, event_name)
    assert result != False
    users = database.find_event_users(event_name)
    assert any([user for user in users if user[1] == user_name2])
    result = database.insert_user(user_name2, user_mention2, event_name)
    assert result == False
    
    #repete para user_name3 -> event_name
    users = database.find_event_users(event_name)
    assert not any([user for user in users if user[1] == user_name3])
    result = database.insert_user(user_name3, user_mention3, event_name)
    assert result != False
    users = database.find_event_users(event_name)
    assert any([user for user in users if user[1] == user_name3])
    result = database.insert_user(user_name3, user_mention3, event_name)
    assert result == False

    # repete para user_name2 -> event_name2
    users = database.find_event_users(event_name2)
    assert not any([u for u in users if u[1] == user_name2])
    result = database.insert_user(user_name2, user_mention2, event_name2)
    assert result != False
    users = database.find_event_users(event_name2)
    assert any([user for user in users if user[1] == user_name2])
    result = database.insert_user(user_name2, user_mention2, event_name2)
    assert result == False

def test_count_event_users():
    # conta quantos usuarios no evento 1
    num_users = database.count_event_users(event_name)
    assert num_users == 3
    num_users2 = database.count_event_users(event_name2)
    assert num_users2 == 1

def test_delete_user():
    # checa se existe no evento 1
    users = database.find_event_users(event_name)
    assert any([user for user in users if user[1] == user_name2])
    # removido do evento 1
    result = database.delete_user(user_mention2, event_name)
    assert result != False
    # checar se ainda existe no evento 1
    users = database.find_event_users(event_name)
    assert not any([user for user in users if user[1] == user_name2]) 
    # checar se user não foi apagado do evento 2
    users2 = database.find_event_users(event_name2)
    assert any([u for u in users2 if u[1] == user_name2]) 

def test_delete_event():
    # checa se o evento existe
    event = database.find_event(event_name)
    event_id = event[0]
    assert event != None
    # tenta deletar com outro usuario
    result = database.delete_event(event_name, user_mention2)
    assert result == False
    # deleta o evento
    result = database.delete_event(event_name, user_mention)
    assert result != False
    # checa se o evento foi apagado
    event = database.find_event(event_name)
    assert event == None

    # repete para evento 2
    event = database.find_event(event_name2)
    event_id = event[0]
    assert event != None
    result = database.delete_event(event_name, user_mention2)
    assert result == False
    result = database.delete_event(event_name2, user_mention)
    assert result != False
    event = database.find_event(event_name2)
    assert event == None

    #checar se todos os usuários foram deletados
    assert database.find_user(user_mention) == []
    assert database.find_user(user_mention2) == []
    assert database.find_user(user_mention3) == []

