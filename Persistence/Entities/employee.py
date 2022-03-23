from user import User

class Employee(User):
    def __init__(self, id, name, email, join_date, is_tl):
        super().__init__(self, id, name, email, join_date)
        self.is_tl = is_tl

    def get_is_tl(self):
        return self.is_tl