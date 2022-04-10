class Response:
    def __init__(self, body, coupon_id, employee_id, review_id, id=0):
        self.id = id
        self.body = body
        self.coupon_id = coupon_id
        self.employee_id = employee_id
        self.review_id = review_id
    
    def get_id(self):
        return self.id

    def get_body(self):
        return self.body
    
    def get_coupon_id(self):
        return self.coupon_id
    
    def get_employee_id(self):
        return self.employee_id

    def get_review_id(self):
        return self.review_id
