from tkinter import *
from tkinter import ttk
from Presentation.fonts import LARGEFONT
from Presentation.helpermethods import populate_menu, populate_table

class AllReviewsView(Frame):
    def __init__(self, parent, controller, service, user):
        Frame.__init__(self, parent)
        self.service = service
        self.user = user

        label = Label(self, text ="All Reviews", font = LARGEFONT)
        label.grid(row = 0, column = 1, padx = 5, pady = 5)
  
        populate_menu(AllReviewsView, controller,self, 1, controller.views)

        set = ttk.Treeview(self)
        set.grid(row = 1, column = 1, padx = 5, pady = 5)

        reviews = list(service.get_all_active_reviews())
        populate_table(reviews, set)