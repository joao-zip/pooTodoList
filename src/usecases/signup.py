from src.usecases.errors.invalidpassworderror import InvalidPasswordError
from src.usecases.errors.duplicateusererror import DuplicateUserError
from src.entities.user import User

class SignUp:
    def __init__(self, userrepo, hash_service) -> None:
        self.userrepo = userrepo
        self.hash_service = hash_service
    
    def perform(self, name, email, password):
        if invalid(password):
            raise InvalidPasswordError()
        if self.userrepo.find_by_email(email) != None:
            raise DuplicateUserError()
        hashed_password = self.hash_service.hash(password)
        user = User(name, email, hashed_password)
        self.userrepo.add(user)


def invalid(password):
    if len(password) < 6 or len(password) > 15:
        return True
    lower_letters = [c for c in password if c.islower()]
    upper_letters = [c for c in password if c.isupper()]
    numbers = [c for c in password if c.isnumeric()]
    alpha = [c for c in password if not c.isalnum()]
    if not lower_letters or not upper_letters or not numbers or not alpha:
        return True
    return False
    