from tkinter import *
from Persistence.Entities.response import Response
from Persistence.Entities.coupon import Coupon
import random
from Presentation.fonts import LARGEFONT
from Presentation.helpermethods import populate_menu, validate_coupon_amount



class NextReviewView(Frame):
    def __init__(self, parent, controller, service, user, data=None):
        Frame.__init__(self, parent)
        self.service = service
        self.user = user
        self.data = data
        self.controller = controller

        label = Label(self, text ="Next Assistance Required Review" if self.data else"Next Review", font = LARGEFONT)
        label.grid(row = 0, column = 1, padx = 5, pady = 5)
  
        populate_menu(NextReviewView, controller,self, 2, controller.views)

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
        

        self.closereviewbutton = Button(self, text="Close", command = self.close_review)
        self.closereviewbutton.grid(row = 10, column = 3, padx = 5, pady = 5)

        self.quitbutton = Button(self, text = "Quit", command=lambda:[self.quit_app(), self.quit()])
        self.quitbutton.grid(row = 10, column = 2, padx = 5, pady = 5)

        #self.testButton = Button(self, text=" test", command=lambda:[funct1(),funct2()])

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

    def on_coupon_value_changed(self, value):
        self.generate_coupon_button["state"] = "normal" if self.coupon_amount_text.get("1.0", END) else "disabled"

    def on_submit(self):
        response = Response(self.responsetext.get("1.0", END), None, self.user.get_id(), self.current_review_id)
        self.current_response_id = self.service.add_response(response)
        self.service.send_email(self.reviewtext.get(), response, self.customer)

        if self.current_coupon_code != None:
            self.service.update_coupon(self.current_coupon_code, self.current_response_id)

        if self.data:
            self.data.pop(0)
            self.set_tl_assistance_required(False)

        if self.controller.employee.get_is_tl():
            self.service.set_close_or_check("CLOSED", self.current_review_id)
            if not self.data:
                self.display_next_review()
        elif random.random() < 0.2:
            self.service.set_close_or_check("MANUAL REVIEW", self.current_review_id)
            self.display_next_review()
        else:
            self.service.set_close_or_check("CLOSED", self.current_review_id)
            self.display_next_review()

        self.coupon_code_text.set("")

    def on_coupon_create(self):
        try:
            amount = self.coupon_amount_text.get("1.0", END).strip()
            self.current_coupon_code = validate_coupon_amount(amount, self.data, self.customer.get_premier())
            couponValue = int(amount)
            self.service.add_coupon(Coupon(self.current_coupon_code, "Pound", couponValue))
            self.coupon_code_text.set("Coupon code is: " + self.current_coupon_code)
            self.responsetext.insert(END, f"\n\nCoupon Code: {self.current_coupon_code}\nCoupon Value: £{couponValue}")
        except Exception as e:
            self.coupon_code_text.set(str(e))

    def get_template_titles(self):
        return self.service.get_template_titles()

    def apply_template(self):
        self.responsetext.delete("1.0", END)
        template = self.service.get_template_by_title(self.chosentemplatetitle.get())
        self.responsetext.insert(END, template.get_body())
        self.on_response_text_changed(template.get_body())
        

    def close_review(self):
        if self.controller.employee.get_is_tl():
            self.service.set_close_or_check("CLOSED", self.current_review_id)
            if not self.data:
                self.display_next_review()
        elif random.random() < 0.2:
            self.service.set_close_or_check("MANUAL REVIEW", self.current_review_id)
            self.display_next_review()
        else:
            self.service.set_close_or_check("CLOSED", self.current_review_id)
            self.display_next_review()


    def quit_app(self):
        self.service.set_close_or_check("NEW", self.current_review_id)
        self.service.clear_checked_out_user(self.current_review_id)