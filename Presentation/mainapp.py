from tkinter import *
from tkinter import ttk
 
LARGEFONT =("Verdana", 35)
  
class tkinterApp(Tk):
     
    def __init__(self, service):
         
        Tk.__init__(self)
         
        container = Frame(self) 
        container.pack(side = "top", fill = "both", expand = True)
  
        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)
  
        self.frames = {} 
  
        for F in (Home, NextReviewView, AllReviewsView, EmployeesView):
            frame = F(container, self, service)
            self.frames[F] = frame
            frame.grid(row = 0, column = 0, sticky ="nsew")
        self.show_frame(Home)
  
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class Home(Frame):
    def __init__(self, parent, controller, service):
        Frame.__init__(self, parent)
        self.service = service
         
        label = Label(self, text ="Constella Review Management", font = LARGEFONT)
        label.grid(row = 0, column = 4, padx = 10, pady = 10)
  
        button1 = Button(self, text ="Next Review",
        command = lambda : controller.show_frame(NextReviewView))
        button1.grid(row = 1, column = 1, padx = 10, pady = 10)
  
        button2 = Button(self, text ="All Reviews",
        command = lambda : controller.show_frame(AllReviewsView))
        button2.grid(row = 2, column = 1, padx = 10, pady = 10)

        button3 = Button(self, text ="Employee View",
        command = lambda : controller.show_frame(EmployeesView))
        button3.grid(row = 3, column = 1, padx = 10, pady = 10)
  
          
class NextReviewView(Frame):
    def __init__(self, parent, controller, service):
        Frame.__init__(self, parent)
        self.service = service

        label = Label(self, text ="Next Review View", font = LARGEFONT)
        label.grid(row = 0, column = 1, padx = 10, pady = 10)
  
        button1 = Button(self, text ="Home", command = lambda : controller.show_frame(Home))
        button1.grid(row = 1, column = 1, padx = 10, pady = 10)
  
        button2 = Button(self, text ="All Reviews", command = lambda : controller.show_frame(AllReviewsView))
        button2.grid(row = 2, column = 1, padx = 10, pady = 10)

        button3 = Button(self, text ="Employees View", command = lambda : controller.show_frame(EmployeesView))
        button3.grid(row = 3, column = 1, padx = 10, pady = 10)

        button4 = Button(self, text ="Next Review", command = self.display_next_review)
        button4.grid(row = 4, column = 4, padx = 10, pady = 10)

        self.reviewtext = StringVar()
        self.reviewtext.set("No review has been selected")
        self.reviewLabel= Label(self, textvariable=self.reviewtext, wraplength=600)
        self.reviewLabel.grid(row = 1, column = 2, padx = 10, pady = 10)

        self.responsetext = Text(self)
        self.responsetext.grid(row = 2, column = 2, padx = 10, pady = 10)

    def display_next_review(self):
        text = self.service.get_next_review().get_body()
        self.reviewtext.set(text)
        print(self.reviewtext)
        
  
  
class AllReviewsView(Frame):
    def __init__(self, parent, controller, service):
        Frame.__init__(self, parent)
        self.service = service

        label = Label(self, text ="All Reviews", font = LARGEFONT)
        label.grid(row = 0, column = 1, padx = 10, pady = 10)
  
        button1 = Button(self, text ="Home", command = lambda : controller.show_frame(Home))
        button1.grid(row = 1, column = 1, padx = 10, pady = 10)
  
        button2 = Button(self, text ="Next Review", command = lambda : controller.show_frame(NextReviewView))
        button2.grid(row = 2, column = 1, padx = 10, pady = 10)

        button3 = Button(self, text ="Employees View", command = lambda : controller.show_frame(EmployeesView))
        button3.grid(row = 3, column = 1, padx = 10, pady = 10)

        set = ttk.Treeview(self)
        set.grid(row = 1, column = 2, padx = 10, pady = 10)

        set['columns']= ('product_title', 'star_rating', 'status', 'title', 'purchase_price', 'created', 'customer_id', 'checked_out_user_id', 'tl_assistance_required')
        set.column("#0", width=0,  stretch=NO)
        # set.column("id",anchor=CENTER, width=80)
        set.column("product_title",anchor=CENTER, width=80)
        # set.column("product_category",anchor=CENTER, width=80)
        set.column("star_rating",anchor=CENTER, width=80)
        set.column("status",anchor=CENTER, width=80)
        set.column("title",anchor=CENTER, width=80)
        # set.column("body",anchor=CENTER, width=80)
        set.column("purchase_price",anchor=CENTER, width=80)
        set.column("created",anchor=CENTER, width=80)
        set.column("customer_id",anchor=CENTER, width=80)
        set.column("checked_out_user_id",anchor=CENTER, width=80)
        set.column("tl_assistance_required",anchor=CENTER, width=80)
        # set.column("importance_score",anchor=CENTER, width=80)

        set.heading("#0",text="",anchor=CENTER)
        # set.heading("id",text="ID",anchor=CENTER)
        set.heading("product_title",text="PRRODUCT TITLE",anchor=CENTER)
        # set.heading("product_category",text="PRODUCT CAT.",anchor=CENTER)
        set.heading("star_rating",text="STAR RATING",anchor=CENTER)
        set.heading("status",text="STATUS",anchor=CENTER)
        set.heading("title",text="TITLE",anchor=CENTER)
        # set.heading("body",text="BODY",anchor=CENTER)
        set.heading("purchase_price",text="PURCHASE PRICE",anchor=CENTER)
        set.heading("created",text="CREATED",anchor=CENTER)
        set.heading("customer_id",text="CUSTOMER ID",anchor=CENTER)
        set.heading("checked_out_user_id",text="CO USER ID",anchor=CENTER)
        set.heading("tl_assistance_required",text="TL ASSISTANCE",anchor=CENTER)
        # set.heading("importance_score",text="IMPORTANCE",anchor=CENTER)

        reviews = list(service.get_reviews(20))
        print(reviews[0])

        for index in range(len(reviews)):
            review = reviews[index]
            set.insert(parent='',index='end', iid=index, text='',
        values=(review.get_product_title(), review.get_star_rating(), review.get_status(), review.get_title(), 
        review.get_purchase_price(), review.get_created(), review.get_customer_id(), review.get_checked_out_user_id(), 
        review.get_tl_assistance_required))


class EmployeesView(Frame):
    def __init__(self, parent, controller, service):
        Frame.__init__(self, parent)
        self.service = service

        label = Label(self, text ="Employees View", font = LARGEFONT)
        label.grid(row = 0, column = 4, padx = 10, pady = 10)
  
        button1 = Button(self, text ="Home", command = lambda : controller.show_frame(Home))
        button1.grid(row = 1, column = 1, padx = 10, pady = 10)
  
        button2 = Button(self, text ="Next Review", command = lambda : controller.show_frame(NextReviewView))
        button2.grid(row = 2, column = 1, padx = 10, pady = 10)

        button3 = Button(self, text ="All Reviews", command = lambda : controller.show_frame(AllReviewsView))
        button3.grid(row = 3, column = 1, padx = 10, pady = 10)
