"""structure models"""
class Users:
    """user model"""
    def __init__(self, name, user_name, password, role):
        self.name = name
        self.user_name = user_name
        self.password = password
        self.role = role

class Login:
    """lgin model"""
    def __init__(self, user_name, password, role):
        self.user_name = user_name
        self.password = password
        self.role = role