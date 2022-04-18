from tkinter import *
from Persistence.Entities.template import Template
from Presentation.fonts import LARGEFONT
from Presentation.helpermethods import populate_menu, populate_table
from Presentation.TLViews.allreviewsview import AllReviewsView

class CreateTemplateView(Frame):
    def __init__(self, parent, controller, service, user):
        Frame.__init__(self, parent)
        self.service = service
        self.user = user
        self.current_review_id = None
        self.controller = controller

        label = Label(self, text ="Create New Template", font = LARGEFONT)
        label.grid(row = 0, column = 1, padx = 5, pady = 5)
  
        populate_menu(CreateTemplateView, controller,self, 1, controller.views)

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
        self.controller.show_frame(AllReviewsView) 

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