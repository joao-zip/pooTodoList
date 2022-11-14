import bcrypt 

class BCryptHashService:
    def __init__(self, salt):
        self.salt = salt
    
    def hash(self, password):
        return bcrypt.hashpw(password.encode("utf-8"), self.salt)
    
    def check(self, password, hashed):
        return bcrypt.checkpw(hashed.encode('uft-8'), password)
    