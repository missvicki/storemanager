"""structure models"""
class Users:
    """user model"""
    def __init__(self, name, user_name, password, role):
        self.name = name
        self.user_name = user_name
        self.password = password
        self.role = role

class Blacklist:
    """blacklist model"""
    def __init__(self, jti):
        self.jti = jti
        