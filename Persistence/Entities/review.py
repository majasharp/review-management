class Review:
    def __init__(self, id, product_title, product_category, star_rating, status, title, body, purchase_price, created, customer_id, checked_out_user_id, tl_assistance_required, importance_score):

        self.id = id
        self.product_title = product_title
        self.product_category = product_category
        self.star_rating = star_rating
        self.status = status
        self.title = title
        self.body = body
        self.purchase_price = purchase_price
        self.created = created
        self.customer_id = customer_id
        self.checked_out_user_id = checked_out_user_id
        self.tl_assistance_required = tl_assistance_required
        self.importance_score = importance_score


    def get_id(self):
        return self.id
    
    def get_product_title(self):
        return self.product_title

    def get_product_category(self):
        return self.product_category

    def get_star_rating(self):
        return self.star_rating

    def get_status(self):
        return self.status

    def get_title(self):
        return self.title

    def get_body(self):
        return self.body

    def get_purchase_price(self):
        return self.purchase_price

    def get_created(self):
        return self.created

    def get_customer_id(self):
        return self.customer_id

    def get_checked_out_user_id(self):
        return self.checked_out_user_id

    def get_tl_assistance_required(self):
        return self.tl_assistance_required

    def get_importance_score(self):
        return self.importance_score

