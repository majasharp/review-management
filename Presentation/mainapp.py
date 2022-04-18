from tkinter import *
from tkinter import ttk
from Persistence.Entities.response import Response
from Persistence.Entities.template import Template
from Persistence.Entities.coupon import Coupon
import random
import string

 
LARGEFONT =("Verdana", 25)
  
class tkinterApp(Tk):
     
    def __init__(self, service):
         
        Tk.__init__(self)
        
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

class TLRequiredReviewsView(Frame):
    def __init__(self, parent, controller, service, user):
        Frame.__init__(self, parent)

        self.service = service
        self.user = user
        self.controller = controller

        label = Label(self, text ="Assistance Required", font = LARGEFONT)
        label.grid(row = 0, column = 1, padx = 5, pady = 5)

        PopulateMenu(TLRequiredReviewsView, controller,self, 1, self.user.get_is_team_leader())

        self.tree = ttk.Treeview(self)
        self.tree.grid(row = 1, column = 1, padx = 5, pady = 5)
        self.reviews = list(service.get_tl_required_reviews())
        populate_table(self.reviews, self.tree)

        self.tree.bind("<Double-1>", self.on_row_selection_changed)

    def on_row_selection_changed(self, event):
        item = int(self.tree.selection()[0])
        # We are providing the NextReview screen with custom data (TL required reviews)
        # The first one should be the row that is clicked on. Therefore, we first insert the item to index 0, and then remove the old
        # index which is now 1 lever higher (thus +1)
        self.reviews.insert(0, self.reviews[item])
        self.reviews.pop(item+1)
        
        self.controller.show_frame(NextReviewView,self.reviews)

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
        user = self.service.get_employee_by_id(userId)
        user.set_is_team_leader(isTeamLeader)
        self.controller.set_user(user)
        self.controller.show_frame(TLRequiredReviewsView if isTeamLeader else NextReviewView)

        
class NextReviewView(Frame):
    def __init__(self, parent, controller, service, user, data=None):
        Frame.__init__(self, parent)
        self.service = service
        self.user = user
        self.data = data

        label = Label(self, text ="Next Assistance Required Review" if self.data else"Next Review", font = LARGEFONT)
        label.grid(row = 0, column = 1, padx = 5, pady = 5)
  
        PopulateMenu(NextReviewView, controller,self, 2, self.user.get_is_team_leader())

        self.current_coupon_code = None

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
        self.premierLabel.grid(row = 1, column = 3, padx = 5, pady = 5)

        self.customername = StringVar()
        self.customernamelabel = Label(self, textvariable=self.customername, wraplength=1000)
        self.customernamelabel.grid(row = 2, column = 3, padx = 5, pady = 5)

        if not self.data:
            self.tl_assistance_button = Button(self, text ="TL assistance required", command = lambda : self.set_tl_assistance_required(True))
            self.tl_assistance_button.grid(row = 3, column = 3, padx = 5, pady = 5)

        self.submit_button = Button(self, text ="Submit response", command = self.on_submit)
        self.submit_button.grid(row = 4, column = 3, padx = 5, pady = 5)
        self.submit_button["state"] = "disabled"

        self.coupon_amount_text = Text(self, height = 1, width = 10)
        self.coupon_amount_text.bind("<Key>", self.on_coupon_value_changed)
        self.coupon_amount_text.grid(row = 5, column = 3, padx = 5, pady = 5)

        self.generate_coupon_button = Button(self, text = "Generate Coupon", command = self.on_coupon_create)
        self.generate_coupon_button.grid(row = 6, column = 3, padx = 0, pady = 0)
        self.generate_coupon_button["state"] = "disabled"

        self.coupon_code_text = StringVar()
        self.coupon_code_label= Label(self, textvariable=self.coupon_code_text, wraplength=100)
        self.coupon_code_label.grid(row = 7, column = 3, padx = 0, pady = 0)

        self.responsetext = Text(self)
        self.responsetext.bind("<Key>", self.on_response_text_changed)
        self.responsetext.grid(row = 4, column = 1, padx = 5, pady = 5)

        self.chosentemplatetitle = StringVar()
        self.chosentemplatetitle.set(list(self.get_template_titles())[0])

        self.templatedropdown = OptionMenu(self, self.chosentemplatetitle, *list(self.get_template_titles()))
        self.templatedropdown.grid(row = 8, column = 3, padx = 5, pady = 5)

        self.templateapplybutton = Button(self, text ="Apply Template", command = self.apply_template)
        self.templateapplybutton.grid(row = 9, column = 3, padx = 5, pady = 5)

        self.display_next_review()


    def display_next_review(self):
        self.responsetext.delete("1.0", END)
        review = self.data[0] if self.data else self.service.get_next_review()
        reviewText = review.get_body()
        reviewTitle = review.get_title()
        reviewProductTitle = review.get_product_title()
        self.current_review_id = review.get_id()
        self.customer = self.service.get_customer_by_id(review.get_customer_id())
        premierText = "Premier Subscriber" if self.customer.get_premier() == 1 else "Not Premier"
        self.customername.set(self.customer.get_name())
        self.reviewtitletext.set(reviewTitle)
        self.reviewtext.set(reviewText)
        self.premiertext.set(premierText)
        self.reviewproducttext.set(reviewProductTitle)

        self.service.set_review_checked_out("CHECKED_OUT", self.user.get_id(), self.current_review_id)

    def set_tl_assistance_required(self, tl_assistance_required):
        self.service.set_tl_assistance_by_id(tl_assistance_required, self.user.get_id(), self.current_review_id)
        self.display_next_review()

    def on_response_text_changed(self, value):
        response = self.responsetext.get("1.0", END)
        self.submit_button["state"] = "normal" if response else "disabled"
        if not self.data:
            self.tl_assistance_button["state"] = "disabled" if response else "normal"

    def on_coupon_value_changed(self, value):
        self.generate_coupon_button["state"] = "normal" if self.coupon_amount_text.get("1.0", END) else "disabled"

    def on_submit(self):
        response = Response(self.responsetext.get("1.0", END), None, self.user.get_id(), self.current_review_id)
        self.current_response_id = self.service.add_response(response)
        self.service.send_email(self.reviewtext.get(), response, self.customer)

        if self.current_coupon_code != None:
            self.service.update_coupon(self.current_coupon_code, self.current_response_id)

        if self.data:
            self.service.set_close_or_check("CLOSED", self.current_review_id)
            self.data.pop(0)
            self.set_tl_assistance_required(False)
        elif random.random() < 0.2:
            self.service.set_close_or_check("MANUAL REVIEW", self.current_review_id)
            self.display_next_review()
        else:
            self.display_next_review()

        self.coupon_code_text.set("")

    def on_coupon_create(self):
        letters = string.ascii_lowercase
        amount = self.coupon_amount_text.get("1.0", END).strip()

        if amount.isdigit(): 
            couponValue = int(amount)
            allowedCouponValue = 10 * (2.5 if self.data else 1) * (2 if self.customer.get_premier() == 1 else 1)
            if couponValue > allowedCouponValue:
                self.coupon_code_text.set(f'The max coupon value available is £{allowedCouponValue}')
            else:    
                self.current_coupon_code = ''.join(random.choice(letters) for i in range(10))
                self.service.add_coupon(Coupon(self.current_coupon_code, "Pound", couponValue))
                self.coupon_code_text.set("Coupon code is: " + self.current_coupon_code)
        else:
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
  
        PopulateMenu(AllReviewsView, controller,self, 1, self.user.get_is_team_leader())

        set = ttk.Treeview(self)
        set.grid(row = 1, column = 1, padx = 5, pady = 5)

        reviews = list(service.get_all_active_reviews())
        populate_table(reviews, set)


class EmployeesView(Frame):
    def __init__(self, parent, controller, service, user):
        Frame.__init__(self, parent)
        self.service = service
        self.user = user
        self.controller = controller
 
        label = Label(self, text ="Employees", font = LARGEFONT)
        label.grid(row = 0, column = 1, padx = 5, pady = 5)
  
        PopulateMenu(EmployeesView, controller,self, 1,self.user.get_is_team_leader())
 
        self.tree = ttk.Treeview(self)
        self.tree.grid(row = 1, column = 1, padx = 5, pady = 5)
        self.employees = list(service.get_all_employees())
        populate_table(self.employees, self.tree)
        
        self.tree.bind("<Double-1>", self.on_row_selection_changed)
 
    def on_row_selection_changed(self, event):
        employeeIdx = int(self.tree.selection()[0])
        self.controller.show_frame(EmployeeReviewsView, self.employees[employeeIdx])
 
 
class EmployeeReviewsView(Frame):
    def __init__(self, parent, controller, service, user, employee):
        Frame.__init__(self, parent)
        self.service = service
        self.user = user
        self.controller = controller
        self.reviews = list(self.service.get_all_reviews_by_employee(employee.get_id()))
        PopulateMenu(EmployeeReviewsView, controller,self, 1, self.user.get_is_team_leader())
        header = "Reviews from Employee " + employee.get_name()
        label = Label(self, text =header, font = LARGEFONT)
        label.grid(row = 0, column = 1, padx = 5, pady = 5)
 
        self.tree = ttk.Treeview(self)
        self.tree.grid(row = 1, column = 1, padx = 5, pady = 5)
        populate_table(self.reviews, self.tree)





class CreateTemplateView(Frame):
    def __init__(self, parent, controller, service, user):
        Frame.__init__(self, parent)
        self.service = service
        self.user = user
        self.current_review_id = None
        self.controller = controller

        label = Label(self, text ="Create New Template", font = LARGEFONT)
        label.grid(row = 0, column = 1, padx = 5, pady = 5)
  
        PopulateMenu(CreateTemplateView, controller,self, 1, self.user.get_is_team_leader())

        self.create_button = Button(self, text ="Create Template", command = self.on_create_template)
        self.create_button.grid(row = 7, column = 0, padx = 5, pady = 5)
        self.create_button["state"] = "disabled"

        self.templatetitle = Text(self, height = 1, width = 30)
        self.templatetitle.bind("<Key>", self.on_template_changed)
        self.templatetitle.grid(row = 1, column = 1, padx = 5, pady = 5)

        self.templatetext = Text(self)
        self.templatetext.bind("<Key>", self.on_template_changed)
        self.templatetext.grid(row = 2, column = 1, padx = 5, pady = 5)

        self.chosentemplatetitle = StringVar(value="Select a template")
        
        self.templatedropdown = OptionMenu(self, self.chosentemplatetitle, *list(self.get_template_titles()))
        self.templatedropdown.grid(row = 8, column = 0, padx=5, pady=5)

        self.loadtemplatebutton = Button(self, text = "Load Template", command = self.load_template)
        self.loadtemplatebutton.grid(row = 9, column = 0, padx= 5, pady=5)

    def on_template_changed(self, value):
        template_title = self.templatetitle.get("1.0", END)
        template = self.templatetext.get("1.0", END)
        self.create_button["state"] = "normal" if template and template_title else "disabled"


    def on_create_template(self):
        self.service.add_template(Template(self.templatetitle.get("1.0", END), self.templatetext.get("1.0", END), self.user.get_id()))
        self.controller.show_frame(Home) 

    def load_template(self):
        self.templatetext.delete("1.0", END)
        self.templatetitle.delete("1.0", END)
        template = self.service.get_template_by_title(self.chosentemplatetitle.get())
        self.templatetext.insert(END, template.get_body())
        self.templatetitle.insert(END, template.get_title())
        self.create_button.configure(text = "Update Template", command = self.update_template)

    def update_template(self):
        self.service.update_template(self.templatetext.get("1.0", END), self.user.get_id(), self.chosentemplatetitle.get())
        self.templatetext.delete("1.0", END)
        self.templatetitle.delete("1.0", END)
        
    def get_template_titles(self):
        return self.service.get_template_titles()



@staticmethod
def PopulateMenu(currentMenuItem, controller, parent, startingRow, isTeamLeader):
    if currentMenuItem !=  LoginView:
        label = Label(parent, text ="REVIEW MANAGEMENT")
        label.grid(row = 0, column = 0, padx = 5, pady = 5)
    
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

    if currentMenuItem !=  TLRequiredReviewsView and isTeamLeader:
        button5 = Button(parent, text ="TL Required Reviews", command = lambda : controller.show_frame(TLRequiredReviewsView))
        button5.grid(row = startingRow + 5, column = 0, padx = 5, pady = 5)

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
            table.heading(col,text=col.replace("_", " ").upper(),anchor=CENTER, command=lambda _col=col: \
            treeview_sort_column(table, _col, False))


    for i in range(len(data)):
        rowData = []
        for attr in cols:
            rowData.append(getattr(data[i], attr))
        table.insert(parent='',index='end', iid=i, text='', values=tuple(rowData))

@staticmethod
def treeview_sort_column(tv, col, reverse):
    l = [(tv.set(k, col), k) for k in tv.get_children('')]
    l.sort(reverse=reverse, key = lambda tup : int(tup[0]) if tup[0].isdigit() else tup[0])

    for index, (val, k) in enumerate(l):
        tv.move(k, '', index)

    tv.heading(col, text=col, command=lambda _col=col: \
        treeview_sort_column(tv, _col, not reverse))
