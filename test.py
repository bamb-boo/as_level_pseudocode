class user:
    def __init__(self, username, email, password):
        self.username=username
        self.__email=email
        self.__password=password
    def get_pass(self):
        return self.__password
    def set_pass(self, password):
        self.__password=password
        
user1=user("dan", "dan123@gmail.com", "123")