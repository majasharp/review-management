class User:
    def __init__(self, id, name, email, join_date):
        self.id = id
        self.first_name = name
        self.email = email
        self.join_date = join_date
    
    def get_id(self):
        return self.id

    def get_name(self):
        return self.first_name
    
    def get_email(self):
        return self.email
    
    def get_join_date(self):
        return self.join_date
