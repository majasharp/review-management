from html import entities
from Persistence.Entities.review import Review
from Presentation.mainapp import tkinterApp
from Persistence.databaseconfig import DataBaseConfigReader
from Persistence.repository import Repository
from service import Service
from nltk.sentiment import SentimentIntensityAnalyzer
from mailconfig import MailConfigReader
from mailservice import MailService
from Presentation.loginview import LoginView
from Presentation.TLViews.allreviewsview import AllReviewsView
from Presentation.nextreviewview import NextReviewView
from Presentation.TLViews.employeesview import EmployeesView
from Presentation.TLViews.createtemplateview import CreateTemplateView
from Presentation.TLViews.tlrequiredreviewsview import TLRequiredReviewsView

def main ():
    dbReader = DataBaseConfigReader()
    emailReader = MailConfigReader()
    dbConfig = dbReader.deserialize('config.json')
    mailConfig = emailReader.deserialize('config.json')
    repository = Repository(dbConfig)

    views = {
        "All Reviews": AllReviewsView,
        "Next Reviews": NextReviewView,
        "Employees": EmployeesView,
        "Templates": CreateTemplateView,
        "Assistance Required":TLRequiredReviewsView
    }

    mail = MailService(mailConfig)
    service = Service(repository, mail)    

    app = tkinterApp(service, views)
    app.mainloop()


    #calculateImportanceScoreNew(service)


def close_positive_reviews(x): #Sets review status to CLOSED if Star_rating > 3
    reader = DataBaseConfigReader()
    config = reader.deserialize('config.json')
    repository = Repository(config)

    sql = "UPDATE review set status = 'CLOSED' where id = (%s)"
    val = (x,)
    repository.update_status_column(sql, val)


def calculateSentimentScore(body):
    reader = DataBaseConfigReader()
    config = reader.deserialize('config.json')
    repository = Repository(config)

    sia = SentimentIntensityAnalyzer()
    sentiment_score = sia.polarity_scores(body)['compound'] #saves compound score result to sentiment_score <-0.005 

    return sentiment_score
 

def calculateImportanceScoreNew(service):
    reader = DataBaseConfigReader()
    config = reader.deserialize('config.json')
    repository = Repository(config)
    service = service

    null_importance_reviews = list(service.get_null_importance_reviews())

    for i in null_importance_reviews:
        star_rating = i.get_star_rating()
        premier = i.get_premier()
        review_id = i.get_id()
        body = i.get_review_body()
        sentiment_score = calculateSentimentScore(body)


        if star_rating == 5:
            base_score = 0
            close_positive_reviews(review_id) #closes this review - don't want to spend time responding to reviews >3 stars
        if star_rating == 4:
            base_score = 0
            close_positive_reviews(review_id)
        if star_rating == 3:
            base_score = 1
        if star_rating == 2:
            base_score = 2
        if star_rating == 1:
            base_score = 3


        if sentiment_score < -0.005: #NTLK considers compound score < -0.005 to be negative. Converts sentiment_score to multiplier for calculating importance_score
            sentiment_multiplier = abs(sentiment_score) + 1 #e.g. converts -0.335 to 1.335 
        else:
            sentiment_multiplier = 1 #if sentiment_score is positive, no multiplier

        if premier == 1:
            importance_score = (base_score * sentiment_multiplier) + 2
        else:
            importance_score = (base_score * sentiment_multiplier)

        service.update_importance_scores(importance_score, review_id)
    repository.rmsdb.close()  



if __name__ == "__main__":
    main()