from tkinter import *
from tkinter import ttk
from Presentation.fonts import LARGEFONT
from Presentation.helpermethods import populate_menu, populate_table
from Presentation.TLViews.employeereviewsview import EmployeeReviewsView

class EmployeesView(Frame):
    def __init__(self, parent, controller, service, user):
        Frame.__init__(self, parent)
        self.service = service
        self.user = user
        self.controller = controller
 
        label = Label(self, text ="Employees", font = LARGEFONT)
        label.grid(row = 0, column = 1, padx = 5, pady = 5)
  
        populate_menu(EmployeesView, controller,self, 1, controller.views)
 
        self.tree = ttk.Treeview(self)
        self.tree.grid(row = 1, column = 1, padx = 5, pady = 5)
        self.employees = list(service.get_all_employees())
        populate_table(self.employees, self.tree)
        
        self.tree.bind("<Double-1>", self.on_row_selection_changed)
 
    def on_row_selection_changed(self, event):
        employeeIdx = int(self.tree.selection()[0])
        self.controller.show_frame(EmployeeReviewsView, self.employees[employeeIdx])