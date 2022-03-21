from user import User

class Customer(User):
    def __init__(self, id, name, email, join_date, premier):
        super().__init__(self, id, name, email, join_date)
        self.premier = premier

    def get_premier(self):
        return self.premier
