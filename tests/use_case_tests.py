from src.usecases.errors.duplicatetodolisterror import DuplicateTodoListError
from src.usecases.errors.invalidcredentialserror import InvalidCredentialsError
from src.usecases.errors.invalidpassworderror import InvalidPasswordError
from src.usecases.errors.duplicateusererror import DuplicateUserError
from src.usecases.errors.invalidusererror import InvalidUserError
from src.entities.errors.duplicateditemerror import DuplicatedItem # Atividade dia 21
from src.usecases.signup import SignUp
from src.usecases.signin import SignIn
from tests.fakehashservice import FakeHashService
import pytest
from src.usecases.createtodolist import CreateTodoList
from src.usecases.createtodoitem import CreateTodoItem
from tests.inmemoryuserrepository import InMemoryUserRepository
from tests.inmemorytodolistrepository import InMemoryTodoListRepository

def test_signup_with_valid_data():
    user_repo = InMemoryUserRepository()
    hash_service = FakeHashService()
    user_name = 'Joe Doe'
    user_email = 'joe@doe.com'
    user_password = 'Test123456789@'
    usecase = SignUp(user_repo, hash_service)
    usecase.perform(user_name, user_email, user_password)
    assert user_repo.find_by_email(user_email).name == user_name

def test_signup_duplicate_user():
    user_repo = InMemoryUserRepository()
    hash_service = FakeHashService()
    user_name = 'Joe Doe'
    user_email = 'joe@doe.com'
    user_password = 'Test12345678@9'
    usecase = SignUp(user_repo, hash_service)
    usecase.perform(user_name, user_email, user_password)
    duplicate_user_name = 'Doe Joe'
    duplicate_user_email = 'joe@doe.com'
    duplicate_user_password = 'Tomalhe@1'
    with pytest.raises(DuplicateUserError):     
        usecase.perform(duplicate_user_name, duplicate_user_email, duplicate_user_password) 

def test_signup_encrypts_password():
    user_repo = InMemoryUserRepository()
    hash_service = FakeHashService()
    user_name = 'Joe Doe'
    user_email = 'joe@doe.com'
    user_password = 'Test123456789@'
    usecase = SignUp(user_repo, hash_service)
    usecase.perform(user_name, user_email, user_password)
    user_in_repo = user_repo.find_by_email(user_email)
    assert user_in_repo.password != user_password
    assert hash_service.check(user_password, user_in_repo.password) == True 

def test_password_lowercase_letter():
    user_repo = InMemoryUserRepository()
    hash_service = FakeHashService()
    user_name = 'Joe Doe'
    user_email = 'joe@doe.com'
    user_password = 'TEST123456789@'
    usecase = SignUp(user_repo, hash_service)
    with pytest.raises(InvalidPasswordError):
        usecase.perform(user_name, user_email, user_password)

def test_password_uppercase_letter():
    user_repo = InMemoryUserRepository()
    hash_service = FakeHashService()
    user_name = 'Joe Doe'
    user_email = 'joe@doe.com'
    user_password = 'test123456789@'
    usecase = SignUp(user_repo, hash_service)
    with pytest.raises(InvalidPasswordError):
        usecase.perform(user_name, user_email, user_password)

def test_password_numbers():
    user_repo = InMemoryUserRepository()
    hash_service = FakeHashService()
    user_name = 'Joe Doe'
    user_email = 'joe@doe.com'
    user_password = 'test@'
    usecase = SignUp(user_repo, hash_service)
    with pytest.raises(InvalidPasswordError):
        usecase.perform(user_name, user_email, user_password)

def test_password_special_character():
    user_repo = InMemoryUserRepository()
    hash_service = FakeHashService()
    user_name = 'Joe Doe'
    user_email = 'joe@doe.com'
    user_password = 'test123456789@'
    usecase = SignUp(user_repo, hash_service)
    with pytest.raises(InvalidPasswordError):
        usecase.perform(user_name, user_email, user_password)

def test_short_password():
    user_repo = InMemoryUserRepository()
    hash_service = FakeHashService()
    user_name = 'Joe Doe'
    user_email = 'joe@doe.com'
    user_password = 'tE89@'
    usecase = SignUp(user_repo, hash_service)
    with pytest.raises(InvalidPasswordError):
        usecase.perform(user_name, user_email, user_password)

def test_long_password():
    user_repo = InMemoryUserRepository()
    hash_service = FakeHashService()
    user_name = 'Joe Doe'
    user_email = 'joe@doe.com'
    user_password = 'tE89@tE89@tE89@A'
    usecase = SignUp(user_repo, hash_service)
    with pytest.raises(InvalidPasswordError):
        usecase.perform(user_name, user_email, user_password)

def test_signin_wrong_password():
    user_repo = InMemoryUserRepository()
    hash_service = FakeHashService()
    user_name = 'Joe Doe'
    user_email = 'joe@doe.com'
    user_password = 'Test123456789@'
    signup = SignUp(user_repo, hash_service)
    signup.perform(user_name, user_email, user_password)
    usecase = SignIn(user_repo, hash_service)
    with pytest.raises(InvalidCredentialsError):
        usecase.perform(user_email, 'WRONG_PASSWORD')

def test_signin_invalid_user():
    user_repo = InMemoryUserRepository()
    hash_service = FakeHashService()
    usecase = SignIn(user_repo, hash_service)
    with pytest.raises(InvalidCredentialsError):
        usecase.perform('invalid@user.com', 'Test123456789@')

def test_successful_todolist_creation():
    user_repo = InMemoryUserRepository()
    hash_service = FakeHashService()
    todo_list_repo = InMemoryTodoListRepository()
    user_name = 'Joe Doe'
    user_email = 'joe@doe.com'
    user_password = 'Test123456789@'
    signup = SignUp(user_repo, hash_service)
    usecase = CreateTodoList(user_repo, todo_list_repo)
    signup.perform(user_name, user_email, user_password)
    usecase.perform(user_email)
    created_todolist = todo_list_repo.find_by_email(user_email)
    assert created_todolist.size() == 0

def test_create_todolist_for_invalid_user():
    user_repo = InMemoryUserRepository()
    todo_list_repo = InMemoryTodoListRepository()
    user_email = 'eu@naotonoemail'
    usecase = CreateTodoList(user_repo, todo_list_repo)
    with pytest.raises(InvalidUserError):
        usecase.perform(user_email)

def test_create_duplicate_todolist():
    user_repo = InMemoryUserRepository()
    hash_service = FakeHashService()
    todo_list_repo = InMemoryTodoListRepository()
    user_name = 'Joe Doe'
    user_email = 'joe@doe.com'
    user_password = 'Test123456789@'
    signup = SignUp(user_repo, hash_service)
    usecase = CreateTodoList(user_repo, todo_list_repo)
    signup.perform(user_name, user_email, user_password)
    usecase.perform(user_email)
    created_todolist = todo_list_repo.find_by_email(user_email)
    with pytest.raises(DuplicateTodoListError):
        usecase.perform(user_email)

def test_create_item_in_todo_list():
    user_repo = InMemoryUserRepository()
    todolist_repo = InMemoryTodoListRepository()
    hash_service = FakeHashService()
    user_name = 'Joe Doe'
    user_email = 'joe@doe.com'
    user_password = 'Test123456789@'
    SignUp(user_repo, hash_service).perform(user_name, user_email, user_password)
    CreateTodoList(user_repo, todolist_repo).perform(user_email)
    usecase = CreateTodoItem(user_repo, todolist_repo)
    item_description = 'call mom'
    item_priority = 0
    usecase.perform(user_email, item_description, item_priority)
    persisted_todo_list = todolist_repo.find_by_email(user_email)
    assert persisted_todo_list.size() == 1
    assert persisted_todo_list.get(0).description == item_description

def test_create_duplicate_item(): # Atividade dia 21
    user_repo = InMemoryUserRepository()
    todolist_repo = InMemoryTodoListRepository()
    hash_service = FakeHashService()
    user_name = 'Joe Doe'
    user_email = 'joe@doe.com'
    user_password = 'Test123456789@'
    SignUp(user_repo, hash_service).perform(user_name, user_email, user_password)
    CreateTodoList(user_repo, todolist_repo).perform(user_email)
    usecase = CreateTodoItem(user_repo, todolist_repo)
    item_description = 'call mom'
    item_priority = 0
    usecase.perform(user_email, item_description, item_priority)
    item2 = 'call mom'
    item2_prio = 0
    with pytest.raises(DuplicatedItem):
        usecase.perform(user_email, item2, item2_prio)
    
def test_create_item_for_invalid_user():
    user_repo = InMemoryUserRepository()
    todo_list_repo = InMemoryTodoListRepository()
    user_email = 'eu@naotonoemail'
    item_description = 'play blackjack'
    item_priority = 0
    usecase = CreateTodoItem(user_repo, todo_list_repo)
    with pytest.raises(InvalidUserError):
        usecase.perform(user_email, item_description, item_priority)

# def test_show_todo_list(): # Atividade dia 24/11
#     user_repo = InMemoryUserRepository()
#     todolist_repo = InMemoryTodoListRepository()
#     hash_service = FakeHashService()
#     user_name = 'Joe Doe'
#     user_email = 'joe@doe.com'
#     user_password = 'Test123456789@'
#     SignUp(user_repo, hash_service).perform(user_name, user_email, user_password)
#     CreateTodoList(user_repo, todolist_repo).perform(user_email)
#     usecase = CreateTodoItem(user_repo, todolist_repo)
#     item_description = 'call mom'
#     item_priority = 0
#     usecase.perform(user_email, item_description, item_priority)
#     item2_description = 'study oop'
#     item2_priority = 1
#     usecase.perform(user_email, item2_description, item2_priority)

# Adicionado o m??todo show na classe TodoList

# def test_change_description():
#     user_repo = InMemoryUserRepository()
#     todolist_repo = InMemoryTodoListRepository()
#     hash_service = FakeHashService()
#     user_name = 'Joe Doe'
#     user_email = 'joe@doe.com'
#     user_password = 'Test123456789@'
#     SignUp(user_repo, hash_service).perform(user_name, user_email, user_password)
#     CreateTodoList(user_repo, todolist_repo).perform(user_email)
#     usecase = CreateTodoItem(user_repo, todolist_repo)
#     item_description = 'call mom'
#     item_priority = 0
#     usecase.perform(user_email, item_description, item_priority)

# def test_change_priority():
#     user_repo = InMemoryUserRepository()
#     todolist_repo = InMemoryTodoListRepository()
#     hash_service = FakeHashService()
#     user_name = 'Joe Doe'
#     user_email = 'joe@doe.com'
#     user_password = 'Test123456789@'
#     SignUp(user_repo, hash_service).perform(user_name, user_email, user_password)
#     CreateTodoList(user_repo, todolist_repo).perform(user_email)
#     usecase = CreateTodoItem(user_repo, todolist_repo)
#     item_description = 'call mom'
#     item_priority = 0
#     usecase.perform(user_email, item_description, item_priority)


