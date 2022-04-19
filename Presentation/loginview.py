from tkinter import *
from Presentation.TLViews.allreviewsview import AllReviewsView
from Presentation.nextreviewview import NextReviewView
from Presentation.TLViews.tlrequiredreviewsview import TLRequiredReviewsView
from Presentation.fonts import LARGEFONT

class LoginView(Frame):
    def __init__(self, parent, controller, service):
        Frame.__init__(self, parent)
        self.service = service
        self.controller = controller
        label = Label(self, text ="Constella Review Management", font = LARGEFONT)
        label.grid(row = 0, column = 1, padx = 5, pady = 5)
        
        isTeamLeaderButton = Button(self, text = "SIGN IN AS TEAM LEADER", command = lambda: self.log_in(True))
        isTeamLeaderButton.grid(column = 2, row = 2, columnspan = 2, sticky = W+E)
        isTeamLeaderButton = Button(self, text = "SIGN IN AS CUSTOMER SERVICE REPRESENTATIVE", command = lambda: self.log_in(False))
        isTeamLeaderButton.grid(column = 2, row = 3, columnspan = 2, sticky = W+E)
    
    def log_in(self, isTeamLeader):
        userId = 1 if isTeamLeader else 2
        employee = self.service.get_employee_by_id(userId)
        employee.set_is_tl(isTeamLeader)
        self.controller.set_employee(employee)
        if not isTeamLeader:
            self.controller.views = {key:val for key, val in self.controller.views.items() if val == NextReviewView}
        
        try:
            self.controller.show_frame(TLRequiredReviewsView if isTeamLeader else NextReviewView)
        except:
            self.controller.show_frame(AllReviewsView)