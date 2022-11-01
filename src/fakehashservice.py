class FakeHashService:
    def hash(self, password):
        return password + 'ugabuga'
    
    def check(self, password, hashed):
        if hashed == password + 'ugabuga':
            return True
        else:
            return False

