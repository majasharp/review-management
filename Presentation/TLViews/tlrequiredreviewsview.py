from tkinter import *
from tkinter import ttk
from Presentation.fonts import LARGEFONT
from Presentation.helpermethods import populate_menu, populate_table
from Presentation.nextreviewview import NextReviewView

class TLRequiredReviewsView(Frame):
    def __init__(self, parent, controller, service, user):
        Frame.__init__(self, parent)

        self.service = service
        self.user = user
        self.controller = controller

        label = Label(self, text ="Assistance Required", font = LARGEFONT)
        label.grid(row = 0, column = 1, padx = 5, pady = 5)

        populate_menu(TLRequiredReviewsView, controller,self, 1, controller.views)

        self.tree = ttk.Treeview(self)
        self.tree.grid(row = 1, column = 1, padx = 5, pady = 5)
        self.reviews = list(service.get_tl_required_reviews())
        populate_table(self.reviews, self.tree)

        self.tree.bind("<Double-1>", self.on_row_selection_changed)

    def on_row_selection_changed(self, event):
        item = int(self.tree.selection()[0])
        # We are providing the NextReview screen with custom data (TL required reviews)
        # The first one should be the row that is clicked on. Therefore, we first insert the item to index 0, and then remove the old
        # index which is now 1 index higher (thus +1)
        self.reviews.insert(0, self.reviews[item])
        self.reviews.pop(item+1)
        
        self.controller.show_frame(NextReviewView,self.reviews)