from tkinter import *
from tkinter import ttk
from Presentation.fonts import LARGEFONT
from Presentation.helpermethods import populate_menu, populate_table

class EmployeeReviewsView(Frame):
    def __init__(self, parent, controller, service, user, employee):
        Frame.__init__(self, parent)
        self.service = service
        self.user = user
        self.controller = controller
        self.reviews = list(self.service.get_all_reviews_by_employee(employee.get_id()))
        populate_menu(EmployeeReviewsView, controller,self, 1, controller.views)
        header = "Reviews from Employee " + employee.get_name()
        label = Label(self, text =header, font = LARGEFONT)
        label.grid(row = 0, column = 1, padx = 5, pady = 5)
 
        self.tree = ttk.Treeview(self)
        self.tree.grid(row = 1, column = 1, padx = 5, pady = 5)
        populate_table(self.reviews, self.tree)