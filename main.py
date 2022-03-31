from html import entities
from Persistence.Entities.review import Review
from Presentation.mainapp import tkinterApp
from Persistence.databaseconfig import DataBaseConfigReader
from Persistence.repository import Repository
from Persistence.queries import SELECT_ALL_REVIEWS, SELECT_ALL_TEST_REVIEWS, SELECT_ALL_USERS
from service import Service
from nltk.sentiment import SentimentIntensityAnalyzer




def main ():
    reader = DataBaseConfigReader()
    config = reader.read_db_config('databaseconfig.json')
    repository = Repository(config)

    service = Service(repository)

    

    app = tkinterApp(service)
    app.mainloop()
   
    ##ignore below - Andrew tinkering
    #allreviews = service.get_all_test_reviews()
    #print(allreviews)
    #review = service.get_next_review
    #id = Review.get_id(review)
    #print(id)
  

    '''allReviews = repository.execute_query(SELECT_ALL_TEST_REVIEWS)
    print(allReviews[0])

    for review in allReviews:
        print(review)
        print("\n")'''

    



def close_positive_reviews(): #Sets review status to CLOSED if Star_rating > 3
    reader = DataBaseConfigReader()
    config = reader.read_db_config('databaseconfig.json')
    repository = Repository(config)

    for x in range(1, 250):
        sql = "SELECT star_rating FROM review_clone_test WHERE id = (%s)"
        val = (x,)

        star_rating = repository.returnSingleRow(sql, val)
        
        if star_rating > 3:
            sql = "UPDATE review_clone_test set status = 'CLOSED' where id = (%s)"
            val = (x,)
            repository.update_status_column(sql, val)


def calculateSentimentScore(x):
    reader = DataBaseConfigReader()
    config = reader.read_db_config('databaseconfig.json')
    repository = Repository(config)

    
    SQL = "SELECT body from review where id = (%s)"
    val = (x,)
    reviewBody = repository.returnSingleRow(SQL, val)

    #print(reviewBody)

    sia = SentimentIntensityAnalyzer()
    sentiment_score = sia.polarity_scores(reviewBody)['compound'] #saves compound score result to sentiment_score
    #print(sentiment_score)
    return sentiment_score
 

    #uncomment below to insert sentiment scores into DB column
    '''SQL = "UPDATE review_clone_test SET sentiment_score = (%s) WHERE id = (%s)" #SQL query to run
    val = (sentiment_score,x) #random sentiment score value to be inserted into sql query and row (x) in which to insert/update

    repository.insert_values(SQL, val) #Send  sql and SS value to insert_values() in repository.py
    repository.rmsdb.close()   '''



def calculateImportanceScore():
    #TODO - NEED MORE EFFICIENT WAY OF PULLING PREMIUM, STAR RATING, AND SENTIMENT_SCORE IN ONE GO, RATHER THAN INDIVIDUALLY
    # Need more efficient way of pulling premium, star_rating and sentiment_score in one, rather than individually
    reader = DataBaseConfigReader()
    config = reader.read_db_config('databaseconfig.json')
    repository = Repository(config)

    for x in range (1, 250): 
        
        #pulls premium-status, star_rating, and sentiment_score of a review as a tuple e.g. (1, 3, -0.241)
        query = "select c.premier from review_clone_test r INNER JOIN customer c on r.customer_id = c.id where r.id = (%s)"
        val = (x,)
        isPremium = repository.returnSingleRow(query, val)
        
        #Pull Reviews star_rating
        query = "select star_rating from review_clone_test where id = (%s)"
        val = (x,)
        star_rating = repository.returnSingleRow(query, val)

        #calculate SentimentScore
        sentiment_score = calculateSentimentScore(x)
        print(sentiment_score)


        if star_rating == 5:
            base_score = 0
        if star_rating == 4:
            base_score = 0
        if star_rating == 3:
            base_score = 1
        if star_rating == 2:
            base_score = 2
        if star_rating == 1:
            base_score = 3
        

        #TODO - Importance_score not being calculated correctly, investigate...
        if sentiment_score < 0: #converts sentiment_score to multiplier for calculating importance_score
            sentiment_multiplier = abs(sentiment_score) + 1 #e.g. converts -0.335 to 1.335 
        else:
            sentiment_multiplier = 1 #if sentiment_score is positive, no multiplier
        


        if isPremium == 1:
            importance_score = (base_score * sentiment_multiplier) + 2
        else:
            importance_score = (base_score * sentiment_multiplier)

        #print(importance_score)



        SQL = "UPDATE review_clone_test SET importance_score = (%s) WHERE id = (%s)" #SQL query to run
        val = (importance_score,x) #random sentiment score value to be inserted into sql query and row (x) in which to insert/update

        repository.insert_values(SQL, val) #Send  sql and SS value to insert_values() in repository.py

    repository.rmsdb.close()  




if __name__ == "__main__":
    main()