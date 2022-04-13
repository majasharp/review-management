class Template:
    def __init__(self, body, last_edited_user_id, id=None):
        self.id = id
        self.body = body
        self.last_edited_user_id = last_edited_user_id
    
    def get_id(self):
        return self.id

    def get_body(self):
        return self.body
    
    def get_last_edited_user_id(self):
        return self.last_edited_user_id
