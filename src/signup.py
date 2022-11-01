from user import User
from duplicateusererror import DuplicateUserError
from fakehashservice import FakeHashService

class SignUp:
    def __init__(self, userrepo, hash_service) -> None:
        self.userrepo = userrepo
        self.hash_service = hash_service
    
    def perform(self, name, email, password):
        if self.userrepo.find_by_email(email) != None:
            raise DuplicateUserError
        hashed_password = self.hash_service.hash(password)
        user = User(name, email, hashed_password)
        self.userrepo.add(user)
