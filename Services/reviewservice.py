from Persistence.queries import SELECT_NEXT_REVIEW
from Persistence.Entities.review import Review

class ReviewService:
    
    def __init__(self, repository):
        self.repository = repository

    def get_next_review(self):
        nextReview = self.repository.execute_query(SELECT_NEXT_REVIEW)[0]
        return Review(nextReview[0], nextReview[1], nextReview[2], nextReview[3], 
            nextReview[4], nextReview[5], nextReview[6], nextReview[7], nextReview[8], 
            nextReview[9], nextReview[10], nextReview[11], nextReview[12])