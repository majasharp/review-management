class Coupon:

    def __init__(self, code, type, value, id=None, response_id=None):
        self.id = id
        self.code = code
        self.type = type
        self.value = value
        self.response_id = response_id
    
    def get_id(self):
        return self.id

    def get_code(self):
        return self.code

    def get_type(self):
        return self.type

    def get_value(self):
        return self.value

    def get_response_id(self):
        return self.response_id