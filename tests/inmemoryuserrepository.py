class InMemoryUserRepository():
    def __init__(self) -> None:
        self.users = []

    def add(self, user):
        self.users.append(user)

    def find_by_email(self, email):
        for e in self.users:
            if e.email == email:
                return e

    