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
  
        for F in (Home, NextReviewView, AllReviewsView, EmployeesView, CreateTemplateView, ):
            frame = F(container, self, service, user)
            self.frames[F] = frame
            frame.grid(row = 0, column = 0, sticky ="nsew")
        self.show_frame(Home)
  
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

class TLRequiredReviewsView(Frame):
    def __init__(self, parent, controller, service, user):
        Frame.__init__(self, parent)
            


class Home(Frame):
    def __init__(self, parent, controller, service, user):
        Frame.__init__(self, parent)
        self.service = service
        self.user = user
         
        label = Label(self, text ="Constella Review Management", font = LARGEFONT)
        label.grid(row = 0, column = 1, padx = 5, pady = 5)
  
        PopulateMenu(Home, controller,self, 1)

        
        button5 = Button(self, text ="TL Required Reviews", 
        command = lambda : controller.show_frame(TLRequiredReviewsView))
        button5.grid(row = 6, column = 0, padx = 5, pady = 5)

          
class NextReviewView(Frame):
    def __init__(self, parent, controller, service, user):
        Frame.__init__(self, parent)
        self.service = service
        self.user = user
        
        label = Label(self, text ="Next Review", font = LARGEFONT)
        label.grid(row = 0, column = 1, padx = 5, pady = 5)
  
        PopulateMenu(NextReviewView, controller,self, 2)

        self.coupon_amount_text = Text(self, height = 1, width = 10)
        self.coupon_amount_text.bind("<Key>", self.on_coupon_value_changed)
        self.coupon_amount_text.grid(row = 7, column = 0, padx = 5, pady = 5)

        self.generate_coupon_button = Button(self, text = "Generate Coupon", command = self.on_coupon_create)
        self.generate_coupon_button.grid(row = 8, column = 0, padx = 0, pady = 0)
        self.generate_coupon_button["state"] = "disabled"

        self.coupon_code_text = StringVar()
        self.coupon_code_label= Label(self, textvariable=self.coupon_code_text, wraplength=100)
        self.coupon_code_label.grid(row = 9, column = 0, padx = 0, pady = 0)

        self.submit_button = Button(self, text ="Submit response", command = self.on_submit)
        self.submit_button.grid(row = 10, column = 0, padx = 5, pady = 5)
        self.submit_button["state"] = "disabled"

        self.tl_assistance_button = Button(self, text ="TL assistance required", command = lambda : self.set_tl_assistance_required(True))
        self.tl_assistance_button.grid(row =6, column = 0, padx = 5, pady = 5)

        self.reviewtitletext = StringVar()
        self.reviewtitlelabel= Label(self, textvariable=self.reviewtitletext, wraplength=1000)
        self.reviewtitlelabel.grid(row = 1, column = 1, padx = 5, pady = 5)

        self.reviewproducttext = StringVar()
        self.reviewproductlabel= Label(self, textvariable=self.reviewproducttext, wraplength=1000)
        self.reviewproductlabel.grid(row = 2, column = 1, padx = 5, pady = 5)

        self.reviewtext = StringVar()
        self.reviewtext.set("No review has been selected")
        self.reviewLabel= Label(self, textvariable=self.reviewtext, wraplength=1000)
        self.reviewLabel.grid(row = 3, column = 1, padx = 5, pady = 5)

        self.premiertext = StringVar()
        self.premierLabel= Label(self, textvariable=self.premiertext, wraplength=1000)
        self.premierLabel.grid(row = 1, column = 0, padx = 5, pady = 5)

        self.responsetext = Text(self)
        self.responsetext.bind("<Key>", self.on_response_text_changed)
        self.responsetext.grid(row = 4, column = 1, padx = 5, pady = 5)

        self.chosentemplatetitle = StringVar()
        self.chosentemplatetitle.set(list(self.get_template_titles())[0])

        self.templatedropdown = OptionMenu(self, self.chosentemplatetitle, *list(self.get_template_titles()))
        self.templatedropdown.grid(row = 11, column = 0, padx = 5, pady = 5)

        self.templateapplybutton = Button(self, text ="Apply Template", command = self.apply_template)
        self.templateapplybutton.grid(row = 12, column = 0, padx = 5, pady = 5)

        self.display_next_review()


    def display_next_review(self):
        self.responsetext.delete("1.0", END)
        review = self.service.get_next_review()
        reviewText = review.get_body()
        reviewTitle = review.get_title()
        reviewProductTitle = review.get_product_title()
        self.current_review_id = review.get_id()
        customer = self.service.get_customer_by_id(review.get_customer_id())
        premierText = "Premier Subscriber" if customer.get_premier() == 1 else "Not Premier"
        self.reviewtitletext.set(reviewTitle)
        self.reviewtext.set(reviewText)
        self.premiertext.set(premierText)
        self.reviewproducttext.set(reviewProductTitle)

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

    def get_template_titles(self):
        return self.service.get_template_titles()

    def apply_template(self):
        self.responsetext.delete("1.0", END)
        template = self.service.get_template_by_title(self.chosentemplatetitle.get())
        self.responsetext.insert(END, template.get_body())
        
    
  
class AllReviewsView(Frame):
    def __init__(self, parent, controller, service, user):
        Frame.__init__(self, parent)
        self.service = service
        self.user = user

        label = Label(self, text ="All Reviews", font = LARGEFONT)
        label.grid(row = 0, column = 1, padx = 5, pady = 5)
  
        PopulateMenu(AllReviewsView, controller,self, 1)

        set = ttk.Treeview(self)
        set.grid(row = 1, column = 1, padx = 5, pady = 5)

        reviews = list(service.get_all_test_reviews())
        populate_table(reviews, set)


class EmployeesView(Frame):
    def __init__(self, parent, controller, service, user):
        Frame.__init__(self, parent)
        self.service = service
        self.user = user

        label = Label(self, text ="Employees", font = LARGEFONT)
        label.grid(row = 0, column = 1, padx = 5, pady = 5)
  
        PopulateMenu(EmployeesView, controller,self, 1)

        set = ttk.Treeview(self)
        set.grid(row = 1, column = 1, padx = 5, pady = 5)
        employees = list(service.get_all_employees())
        populate_table(employees, set)




class CreateTemplateView(Frame):
    def __init__(self, parent, controller, service, user):
        Frame.__init__(self, parent)
        self.service = service
        self.user = user
        self.current_review_id = None
        self.controller = controller

        label = Label(self, text ="Create New Template", font = LARGEFONT)
        label.grid(row = 0, column = 1, padx = 5, pady = 5)
  
        PopulateMenu(CreateTemplateView, controller,self, 1)

        self.create_button = Button(self, text ="Create Template", command = self.on_create_template)
        self.create_button.grid(row = 6, column = 0, padx = 5, pady = 5)
        self.create_button["state"] = "disabled"

        self.templatetitle = Text(self, height = 1, width = 30)
        self.templatetitle.bind("<Key>", self.on_template_changed)
        self.templatetitle.grid(row = 1, column = 1, padx = 5, pady = 5)

        self.templatetext = Text(self)
        self.templatetext.bind("<Key>", self.on_template_changed)
        self.templatetext.grid(row = 2, column = 1, padx = 5, pady = 5)

    def on_template_changed(self, value):
        template_title = self.templatetitle.get("1.0", END)
        template = self.templatetext.get("1.0", END)
        self.create_button["state"] = "normal" if template and template_title else "disabled"


    def on_create_template(self):
        self.service.add_template(Template(self.templatetitle.get("1.0", END), self.templatetext.get("1.0", END), self.user.get_id()))
        self.controller.show_frame(Home) 



@staticmethod
def PopulateMenu(currentMenuItem, controller, parent, startingRow):
    if currentMenuItem !=  Home:
        button1 = Button(parent, text ="Home", command = lambda : controller.show_frame(Home))
        button1.grid(row = startingRow, column = 0, padx = 5, pady = 5)
    
    if currentMenuItem !=  AllReviewsView:
        button2 = Button(parent, text ="All Reviews", command = lambda : controller.show_frame(AllReviewsView))
        button2.grid(row = startingRow + 1, column = 0, padx = 5, pady = 5)

    if currentMenuItem !=  NextReviewView:
        button3 = Button(parent, text ="Next Review", command = lambda : controller.show_frame(NextReviewView))
        button3.grid(row = startingRow + 2, column = 0, padx = 5, pady = 5)

    if currentMenuItem !=  EmployeesView:
        button4 = Button(parent, text ="Employees", command = lambda : controller.show_frame(EmployeesView))
        button4.grid(row = startingRow + 3, column = 0, padx = 5, pady = 5)

    if currentMenuItem !=  CreateTemplateView:
        button5 = Button(parent, text ="Create New Template", command = lambda : controller.show_frame(CreateTemplateView))
        button5.grid(row = startingRow + 4, column = 0, padx = 5, pady = 5)

@staticmethod
def populate_table(data, table):
    table.heading("#0",text="",anchor=CENTER)
    table.column("#0", width=0,  stretch=NO)
    cols= []

    for attr, value in data[0].__dict__.items():
        if attr != 'id':
            cols.append(attr)

    table['columns']= tuple(cols)

    for col in cols:
        if attr != 'id':
            table.column(col,anchor=CENTER, width=80)
            table.heading(col,text=col.replace("_", " ").upper(),anchor=CENTER)


    for i in range(len(data)):
        rowData = []
        for attr in cols:
            rowData.append(getattr(data[i], attr))
        table.insert(parent='',index='end', iid=i, text='', values=tuple(rowData))



