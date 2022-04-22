class CustomerReview:

    def __init__(self, id, star_rating, premier, review_body):
        self.id = id
        self.star_rating = star_rating
        self.premier = premier
        self.review_body = review_body

    def get_id(self):
        return self.id

    def get_star_rating(self):
        return self.star_rating

    def get_premier(self):
        return self.premier

    def get_review_body(self):
        return self.review_body


