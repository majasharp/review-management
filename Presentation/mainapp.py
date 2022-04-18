from tkinter import *
from Presentation.loginview import LoginView

class tkinterApp(Tk):
     
    def __init__(self, service, views):
        Tk.__init__(self)
        
        self.views = views
        self.service = service 
        self.container = Frame(self)
        self.container.pack(side = "top", fill = "both", expand = True)
        super().geometry('1400x700')
  
        self.container.grid_rowconfigure(0, weight = 1)
        self.container.grid_columnconfigure(0, weight = 1)
        
        self.user = None
        self.show_frame(LoginView)

    def show_frame(self, view, data=None):
        if view is LoginView:
            frame = view(self.container, self, self.service)
        elif data:
            frame = view(self.container, self, self.service, self.user, data)
        else:
            frame = view(self.container, self, self.service, self.user)
        frame.grid(row = 0, column = 0, sticky ="nsew")
        frame.tkraise()

    def set_user(self, user):
        self.user = user