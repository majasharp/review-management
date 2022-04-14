from Persistence.Entities.user import User

class Customer(User):
    def __init__(self, id, name, email, join_date, premier):
        super().__init__(id, name, email, join_date)
        self.premier = premier

    def get_premier(self):
        return self.premier
