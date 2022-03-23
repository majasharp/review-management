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




    """ for x in range (15):
        random_sentiment = round(random.uniform(-1, 1), 3)
        print(random_sentiment) """


    for x in range (1):
        random_sentiment = round(random.uniform(-1, 1), 3) #Generate random sentiment score between -1 and 1
        SQL = "UPDATE review_clone_test SET sentiment_score = (%s) WHERE id = 1" #SQL query to run
        val = (random_sentiment) #random sentiment score value to be inserted into sql query

        repository.insert_values(SQL, val) #Send  sql and SS value to insert_values() in repository.py
        repository.rmsdb.commit()


        repository.rmsdb.close()




if __name__ == "__main__":
    main()