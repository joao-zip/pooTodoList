from invalidcredentialserror import InvalidCredentialsError
from user import User

class SignIn:
    def __init__(self, user_repo, hash_service) -> None:
        self.user_repo = user_repo
        self.hash_service = hash_service

    def perform(self, email, password):
        user = self.user_repo.find_by_email(email)
        if not user:
            raise InvalidCredentialsError()
        if self.hash_service.check(password, user.password): 
            return True
        raise InvalidCredentialsError()
