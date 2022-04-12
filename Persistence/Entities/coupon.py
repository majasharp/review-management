from msilib.schema import TypeLib


class coupon:

    def __init__(self, id, coupon_code, type, coupon_value, response_id):
        self.id = id
        self.coupon_code = coupon_code
        self.type = type
        self.coupon_value = coupon_value
        self.response_id = response_id

    
    def get_id(self):
        return self.id


    def get_coupon_code(self):
        return self.coupon_code

    def get_type(self):
        return self.type

    def get_coupon_value(self):
        return self.coupon_value

    def get_response_id(self):
        return self.response_id