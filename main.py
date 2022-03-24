
from Persistence.databaseconfig import DataBaseConfigReader
from Persistence.repository import Repository
from Persistence.queries import SELECT_ALL_REVIEWS, SELECT_ALL_TEST_REVIEWS, SELECT_ALL_USERS
import random


def main ():
    reader = DataBaseConfigReader()
    config = reader.read_db_config('databaseconfig.json')
    repository = Repository(config)



    """  results = repository.execute_query(SELECT_ALL_REVIEWS)
    for result in results:
        print(result)
    
    userresults = repository.execute_query(SELECT_ALL_USERS)
    for users in userresults:
        print(users) 

    testreviewresults = repository.execute_query(SELECT_ALL_TEST_REVIEWS)
    for review in testreviewresults:
        print(review)
        """
    #insertRandomSentimentScore() #Do not run insertRandomSentimentScore() without also running calculateImportanceScore()
    calculateImportanceScore()



    

def insertRandomSentimentScore(): #If you run this, also run calculateImportanceScore() to update importance_score values in DB to match

    reader = DataBaseConfigReader()
    config = reader.read_db_config('databaseconfig.json')
    repository = Repository(config)

    for x in range (1, 250): #loops through 10 rows in review_clone_test:
        random_sentiment = round(random.uniform(-1, 1), 3) #Generate random sentiment score between -1 and 1, rounded to 3 decimal places
        SQL = "UPDATE review_clone_test SET sentiment_score = (%s) WHERE id = (%s)" #SQL query to run
        val = (random_sentiment,x) #random sentiment score value to be inserted into sql query and row (x) in which to insert/update

        repository.insert_values(SQL, val) #Send  sql and SS value to insert_values() in repository.py
    
   
    repository.rmsdb.close()   






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

        #pull review sentiment_score
        query = "select sentiment_score from review_clone_test where id = (%s)"
        val = (x,)
        sentiment_score = repository.returnSingleRow(query, val)

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
            sentiment_multiplier = sentiment_score + 2 #e.g. converts -0.335 to 1.335 
        else:
            sentiment_multiplier = 1
        #print(str(isPremium) + " " + str(star_rating) + " " + str(sentiment_score))

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