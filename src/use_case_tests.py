from inmemoryuserrepository import InMemoryUserRepository
from invalidpassworderror import InvalidPasswordError
from signup import SignUp
from duplicateusererror import DuplicateUserError
from fakehashservice import FakeHashService
from bcrypthashservice import BCryptHashService
import pytest
import bcrypt

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
