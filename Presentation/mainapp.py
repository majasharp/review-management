from tkinter import *
from tkinter import ttk
from Persistence.Entities.response import Response
from Persistence.Entities.template import Template
from Persistence.Entities.coupon import Coupon
import random
import string

 
LARGEFONT =("Verdana", 25)
  
class tkinterApp(Tk):
     
    def __init__(self, service, user):
         
        Tk.__init__(self)
         
        container = Frame(self) 
        container.pack(side = "top", fill = "both", expand = True)

        super().geometry('1400x700')
  
        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)
  
        self.frames = {} 
  
        for F in (Home, NextReviewView, AllReviewsView, EmployeesView, CreateTemplateView):
            frame = F(container, self, service, user)
            self.frames[F] = frame
            frame.grid(row = 0, column = 0, sticky ="nsew")
        self.show_frame(Home)
  
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class Home(Frame):
    def __init__(self, parent, controller, service, user):
        Frame.__init__(self, parent)
        self.service = service
        self.user = user
         
        label = Label(self, text ="Constella Review Management", font = LARGEFONT)
        label.grid(row = 0, column = 1, padx = 5, pady = 5)
  
        button1 = Button(self, text ="Next Review",
        command = lambda : controller.show_frame(NextReviewView))
        button1.grid(row = 1, column = 0, padx = 5, pady = 5)
  
        button2 = Button(self, text ="All Reviews",
        command = lambda : controller.show_frame(AllReviewsView))
        button2.grid(row = 2, column = 0, padx = 5, pady = 5)

        button3 = Button(self, text ="Employee View",
        command = lambda : controller.show_frame(EmployeesView))
        button3.grid(row = 3, column = 0, padx = 5, pady = 5)

        button4 = Button(self, text ="Create New Template", 
        command = lambda : controller.show_frame(CreateTemplateView))
        button4.grid(row = 4, column = 0, padx = 5, pady = 5)
  
          
class NextReviewView(Frame):
    def __init__(self, parent, controller, service, user):
        Frame.__init__(self, parent)
        self.service = service
        self.user = user
        
        label = Label(self, text ="Next Review View", font = LARGEFONT)
        label.grid(row = 0, column = 1, padx = 5, pady = 5)
  
        button1 = Button(self, text ="Home", command = lambda : controller.show_frame(Home))
        button1.grid(row = 1, column = 0, padx = 5, pady = 5)
  
        button2 = Button(self, text ="All Reviews", command = lambda : controller.show_frame(AllReviewsView))
        button2.grid(row = 2, column = 0, padx = 5, pady = 5)

        button3 = Button(self, text ="Employees View", command = lambda : controller.show_frame(EmployeesView))
        button3.grid(row = 3, column = 0, padx = 5, pady = 5)

        button4 = Button(self, text ="Create New Template", command = lambda : controller.show_frame(CreateTemplateView))
        button4.grid(row = 4, column = 0, padx = 5, pady = 5)

        self.coupon_amount_text = Text(self, height = 1, width = 10)
        self.coupon_amount_text.bind("<Key>", self.on_coupon_value_changed)
        self.coupon_amount_text.grid(row = 8, column = 0, padx = 5, pady = 5)

        self.generate_coupon_button = Button(self, text = "Generate Coupon", command = self.on_coupon_create)
        self.generate_coupon_button.grid(row = 7, column = 0, padx = 0, pady = 0)
        self.generate_coupon_button["state"] = "disabled"

        self.coupon_code_text = StringVar()

        self.coupon_code_label= Label(self, textvariable=self.coupon_code_text, wraplength=100)
        self.coupon_code_label.grid(row = 9, column = 0, padx = 0, pady = 0)

        self.submit_button = Button(self, text ="Submit response", command = self.on_submit)
        self.submit_button.grid(row = 4, column = 3, padx = 5, pady = 5)
        self.submit_button["state"] = "disabled"

        self.tl_assistance_button = Button(self, text ="TL assistance required", command = lambda : self.set_tl_assistance_required(True))
        self.tl_assistance_button.grid(row =5, column = 0, padx = 5, pady = 5)

        self.reviewtext = StringVar()
        self.reviewtext.set("No review has been selected")

        self.reviewLabel= Label(self, textvariable=self.reviewtext, wraplength=1000)
        self.reviewLabel.grid(row = 1, column = 1, padx = 5, pady = 5)

        self.responsetext = Text(self)
        self.responsetext.bind("<Key>", self.on_response_text_changed)
        self.responsetext.place(
            x = 150,
            y = 200,
            width=1000,
            height=300)
        self.display_next_review()


    def display_next_review(self):
        self.responsetext.delete("1.0", END)
        review = self.service.get_next_review()
        text = review.get_body()
        self.current_review_id = review.get_id()
        self.reviewtext.set(text)

        self.service.set_review_status("CHECKED_OUT", self.user.get_id(), self.current_review_id)

    def set_tl_assistance_required(self, tl_assistance_required):
        self.service.set_tl_assistance_by_id(tl_assistance_required, self.current_review_id)
        self.display_next_review()

    def on_response_text_changed(self, value):
        response = self.responsetext.get("1.0", END)
        self.submit_button["state"] = "normal" if response else "disabled"
        self.tl_assistance_button["state"] = "disabled" if response else "normal"

    def on_coupon_value_changed(self, value):
        coupon_amount = self.coupon_amount_text.get("1.0", END)
        self.generate_coupon_button["state"] = "normal" if coupon_amount else "disabled"

    def on_submit(self):
        self.current_response_id = self.service.add_response(Response(self.responsetext.get("1.0", END), None, self.user.get_id(), self.current_review_id))

        if self.current_coupon_code != None:
            self.service.update_coupon(self.current_coupon_code, self.current_response_id)
        self.display_next_review()
        self.coupon_code_text.set("")

    def on_coupon_create(self):
        letters = string.ascii_lowercase
        self.current_coupon_code = ''.join(random.choice(letters) for i in range(10))

        try: 
            self.service.add_coupon(Coupon(self.current_coupon_code, "Pound", int(self.coupon_amount_text.get("1.0",END))))
            self.coupon_code_text.set("Coupon code is: " + self.current_coupon_code)
        except:
            self.coupon_code_text.set("You must enter a number as a coupon value")
        
    
  
class AllReviewsView(Frame):
    def __init__(self, parent, controller, service, user):
        Frame.__init__(self, parent)
        self.service = service
        self.user = user

        label = Label(self, text ="All Reviews", font = LARGEFONT)
        label.grid(row = 0, column = 1, padx = 5, pady = 5)
  
        button1 = Button(self, text ="Home", command = lambda : controller.show_frame(Home))
        button1.grid(row = 1, column = 1, padx = 5, pady = 5)
  
        button2 = Button(self, text ="Next Review", command = lambda : controller.show_frame(NextReviewView))
        button2.grid(row = 2, column = 1, padx = 5, pady = 5)

        button3 = Button(self, text ="Employees View", command = lambda : controller.show_frame(EmployeesView))
        button3.grid(row = 3, column = 1, padx = 5, pady = 5)

        button4 = Button(self, text ="Create New Template", command = lambda : controller.show_frame(CreateTemplateView))
        button4.grid(row = 4, column = 0, padx = 5, pady = 5)

        set = ttk.Treeview(self)
        set.grid(row = 1, column = 2, padx = 5, pady = 5)

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

        reviews = list(service.get_all_test_reviews())

        for index in range(len(reviews)):
            review = reviews[index]
            set.insert(parent='',index='end', iid=index, text='',
        values=(review.get_product_title(), review.get_star_rating(), review.get_status(), review.get_title(), 
        review.get_purchase_price(), review.get_created(), review.get_customer_id(), review.get_checked_out_user_id(), 
        review.get_tl_assistance_required()))


class EmployeesView(Frame):
    def __init__(self, parent, controller, service, user):
        Frame.__init__(self, parent)
        self.service = service
        self.user = user

        label = Label(self, text ="Employees View", font = LARGEFONT)
        label.grid(row = 0, column = 1, padx = 5, pady = 5)
  
        button1 = Button(self, text ="Home", command = lambda : controller.show_frame(Home))
        button1.grid(row = 1, column = 1, padx = 5, pady = 5)
  
        button2 = Button(self, text ="Next Review", command = lambda : controller.show_frame(NextReviewView))
        button2.grid(row = 2, column = 1, padx = 5, pady = 5)

        button3 = Button(self, text ="All Reviews", command = lambda : controller.show_frame(AllReviewsView))
        button3.grid(row = 3, column = 1, padx = 5, pady = 5)

        button4 = Button(self, text ="Create New Template", command = lambda : controller.show_frame(CreateTemplateView))
        button4.grid(row = 4, column = 0, padx = 5, pady = 5)

        set = ttk.Treeview(self)
        set.grid(row = 1, column = 2, padx = 5, pady = 5)

        set['columns']= ('id', 'name', 'email', 'join_date', 'is_tl')
        set.column("#0", width=0,  stretch=NO)
        set.column("id",anchor=CENTER, width=120)
        set.column("name",anchor=CENTER, width=120)
        set.column("email",anchor=CENTER, width=120)
        set.column("join_date",anchor=CENTER, width=120)
        set.column("is_tl",anchor=CENTER, width=120)

        set.heading("#0",text="",anchor=CENTER)
        set.heading("id",text="ID",anchor=CENTER)
        set.heading("name",text="NAME",anchor=CENTER)
        set.heading("email",text="EMAIL",anchor=CENTER)
        set.heading("join_date",text="JOIN_DATE",anchor=CENTER)
        set.heading("is_tl",text="IS_TL",anchor=CENTER)

        employees = list(service.get_all_employees())

        for index in range(len(employees)):
            employee = employees[index]
            set.insert(parent='',index='end', iid=index, text='',
        values=(employee.get_id(), employee.get_name(), employee.get_email(), employee.get_join_date(), 
        employee.get_is_tl()))


class CreateTemplateView(Frame):
    def __init__(self, parent, controller, service, user):
        Frame.__init__(self, parent)
        self.service = service
        self.user = user
        self.current_review_id = None
        self.controller = controller

        label = Label(self, text ="Create New Template", font = LARGEFONT)
        label.grid(row = 0, column = 1, padx = 5, pady = 5)
  
        button1 = Button(self, text ="Home", command = lambda : controller.show_frame(Home))
        button1.grid(row = 1, column = 0, padx = 5, pady = 5)
  
        button2 = Button(self, text ="All Reviews", command = lambda : controller.show_frame(AllReviewsView))
        button2.grid(row = 2, column = 0, padx = 5, pady = 5)

        button3 = Button(self, text ="Employees View", command = lambda : controller.show_frame(EmployeesView))
        button3.grid(row = 3, column = 0, padx = 5, pady = 5)

        button4 = Button(self, text ="Next Review", command = lambda : controller.show_frame(NextReviewView))
        button4.grid(row = 4, column = 0, padx = 5, pady = 5)

        self.create_button = Button(self, text ="Create Template", command = self.on_create_template)
        self.create_button.grid(row = 4, column = 3, padx = 5, pady = 5)
        self.create_button["state"] = "disabled"

        self.templatetitle = Text(self, height = 1, width = 30)
        self.templatetitle.bind("<Key>", self.on_template_changed)
        self.templatetitle.grid(row = 5, column = 3, padx = 5, pady = 5)

        self.templatetext = Text(self)
        self.templatetext.bind("<Key>", self.on_template_changed)
        self.templatetext.place(
            x = 150,
            y = 250,
            width=1000,
            height=300)

    def on_template_changed(self, value):
        template_title = self.templatetitle.get("1.0", END)
        template = self.templatetext.get("1.0", END)
        self.create_button["state"] = "normal" if template and template_title else "disabled"


    def on_create_template(self):
        self.service.add_template(Template(self.templatetitle.get("1.0", END), self.templatetext.get("1.0", END), self.user.get_id()))
        self.controller.show_frame(Home) 

