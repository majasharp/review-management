import asyncio
from Persistence.commands import SET_STATUS_CLOSED
from Persistence.queries import SELECT_ALL_REVIEWS_BY_EMPLOYEE
from Presentation.mainapp import tkinterApp
from Persistence.databaseconfig import DataBaseConfigReader
from Persistence.repository import Repository
from service import Service
from mailconfig import MailConfigReader
from mailservice import MailService
from Presentation.loginview import LoginView
from Presentation.TLViews.allreviewsview import AllReviewsView
from Presentation.nextreviewview import NextReviewView
from Presentation.TLViews.employeesview import EmployeesView
from Presentation.TLViews.createtemplateview import CreateTemplateView
from Presentation.TLViews.tlrequiredreviewsview import TLRequiredReviewsView
import nltk

def main():
    # Please execute this line of code and install package "vader lexicon" in the right directory.
    # In case you are unsure of the correct directory, please run the application without executing this method. It will then state the directories it's looked in
    # Copy that directory, run this method, select vader lexicon, copy paste the desired directory folder into the correct textfield and press download
    # Restart the application and it works! (In case you do not do this step, the sentiments will not be calculated and ingested - this is done in a background job
    # and will therefore not cause any issues for the user's current session)
    def setup_nltk():
        nltk.download()
    
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
    
    backgroundService = Service(Repository(dbConfig), MailService(mailConfig))    

    # Set all positive reviews closed
    repository.execute_command(SET_STATUS_CLOSED, (3,))
    #backgroundService.update_importance_scores() #This happens in the background so as to not block the main thread, see comment above. It has its own repository and service to avoid problems.

    app = tkinterApp(service, views)
    app.mainloop()


if __name__ == "__main__":
    main()

    
