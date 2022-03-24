import tkinter as tk
from tkinter import ttk
  
 
LARGEFONT =("Verdana", 35)
  
class tkinterApp(tk.Tk):
     
    def __init__(self, *args, **kwargs):
         
        tk.Tk.__init__(self, *args, **kwargs)
         
        container = tk.Frame(self) 
        container.pack(side = "top", fill = "both", expand = True)
  
        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)
  
        self.frames = {} 
  
        for F in (Home, NextReviewView, AllReviewsView, EmployeesView):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row = 0, column = 0, sticky ="nsew")
        self.show_frame(Home)
  
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class Home(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
         
        label = ttk.Label(self, text ="Constella Review Management", font = LARGEFONT)
        label.grid(row = 0, column = 4, padx = 10, pady = 10)
  
        button1 = ttk.Button(self, text ="Next Review",
        command = lambda : controller.show_frame(NextReviewView))
        button1.grid(row = 1, column = 1, padx = 10, pady = 10)
  
        button2 = ttk.Button(self, text ="All Reviews",
        command = lambda : controller.show_frame(AllReviewsView))
        button2.grid(row = 2, column = 1, padx = 10, pady = 10)

        button3 = ttk.Button(self, text ="Employee View",
        command = lambda : controller.show_frame(EmployeesView))
        button3.grid(row = 3, column = 1, padx = 10, pady = 10)
  
          
class NextReviewView(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text ="Next Review View", font = LARGEFONT)
        label.grid(row = 0, column = 4, padx = 10, pady = 10)
  
        button1 = ttk.Button(self, text ="Home", command = lambda : controller.show_frame(Home))
        button1.grid(row = 1, column = 1, padx = 10, pady = 10)
  
        button2 = ttk.Button(self, text ="All Reviews", command = lambda : controller.show_frame(AllReviewsView))
        button2.grid(row = 2, column = 1, padx = 10, pady = 10)

        button3 = ttk.Button(self, text ="Employees View", command = lambda : controller.show_frame(EmployeesView))
        button3.grid(row = 3, column = 1, padx = 10, pady = 10)
  
  
class AllReviewsView(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text ="All Reviews", font = LARGEFONT)
        label.grid(row = 0, column = 4, padx = 10, pady = 10)
  
        button1 = ttk.Button(self, text ="Home", command = lambda : controller.show_frame(Home))
        button1.grid(row = 1, column = 1, padx = 10, pady = 10)
  
        button2 = ttk.Button(self, text ="Next Review", command = lambda : controller.show_frame(NextReviewView))
        button2.grid(row = 2, column = 1, padx = 10, pady = 10)

        button3 = ttk.Button(self, text ="Employees View", command = lambda : controller.show_frame(EmployeesView))
        button3.grid(row = 3, column = 1, padx = 10, pady = 10)


class EmployeesView(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text ="Employees View", font = LARGEFONT)
        label.grid(row = 0, column = 4, padx = 10, pady = 10)
  
        button1 = ttk.Button(self, text ="Home", command = lambda : controller.show_frame(Home))
        button1.grid(row = 1, column = 1, padx = 10, pady = 10)
  
        button2 = ttk.Button(self, text ="Next Review", command = lambda : controller.show_frame(NextReviewView))
        button2.grid(row = 2, column = 1, padx = 10, pady = 10)

        button3 = ttk.Button(self, text ="All Reviews", command = lambda : controller.show_frame(AllReviewsView))
        button3.grid(row = 3, column = 1, padx = 10, pady = 10)
  
app = tkinterApp()
app.mainloop()