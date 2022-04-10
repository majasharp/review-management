from Persistence.queries import CALC_IMPORTANCE_VALUES, SELECT_NEXT_REVIEW, SELECT_REVIEW_BY_ID, SELECT_ALL_TEST_REVIEWS, SELECT_ALL_EMPLOYEES
from Persistence.Entities.review import Review
from Persistence.Entities.employee import Employee

class Service:
    
    def __init__(self, repository):
        self.repository = repository

    def get_next_review(self):
        nextReview = self.repository.execute_query(SELECT_NEXT_REVIEW)[0]
        return Review(nextReview[0], nextReview[1], nextReview[2], nextReview[3], 
            nextReview[4], nextReview[5], nextReview[6], nextReview[7], nextReview[8], 
            nextReview[9], nextReview[10], nextReview[11], nextReview[12])

    def get_all_test_reviews(self):
        reviews = self.repository.execute_query(SELECT_ALL_TEST_REVIEWS)
        return map(lambda review: Review(review[0], review[1], review[2], review[3], 
            review[4], review[5], review[6], review[7], review[8], 
            review[9], review[10], review[11], review[12]), reviews)


    def get_specific_review(self, reviewID):
        review = self.repository.get_rows(SELECT_REVIEW_BY_ID, (reviewID,))
        return Review(review[0], review[1], review[2], review[3], 
            review[4], review[5], review[6], review[7], review[8], 
            review[9], review[10], review[11], review[12])

    def get_importance_calc_values(self):
        reviews = self.repository.execute_query(CALC_IMPORTANCE_VALUES)
        return map(lambda review: Review(review[0], review[1], review[2], review[3], 
            review[4], review[5], review[6], review[7], review[8], 
            review[9], review[10], review[11], review[12]), reviews)

    def get_all_employees(self):
        employees = self.repository.execute_query(SELECT_ALL_EMPLOYEES)
        return map(lambda employee: Employee(employee[0], employee[1], employee[2], employee[3], employee[4]), employees)