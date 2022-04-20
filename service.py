from email import message
from Persistence.Entities.customerreview import CustomerReview
from Persistence.queries import *
from Persistence.commands import *
from Persistence.Entities.review import Review
from Persistence.Entities.employee import Employee
from Persistence.Entities.customer import Customer
from Persistence.Entities.template import Template
import asyncio

class Service:
    
    def __init__(self, repository, mail):
        self.repository = repository
        self.mail = mail

    def get_next_review(self):
        nextReview = self.repository.execute_query(SELECT_NEXT_REVIEW)[0]
        return Review(nextReview[0], nextReview[1], nextReview[2], nextReview[3], 
            nextReview[4], nextReview[5], nextReview[6], nextReview[7], nextReview[8], 
            nextReview[9], nextReview[10], nextReview[11], nextReview[12])

    def get_all_active_reviews(self):
        reviews = self.repository.execute_query(SELECT_ACTIVE_REVIEWS)
        return map(lambda review: Review(review[0], review[1], review[2], review[3], 
            review[4], review[5], review[6], review[7], review[8], 
            review[9], review[10], review[11], review[12]), reviews)

    def get_all_reviews_by_employee(self, id):
        reviews = self.repository.execute_query(SELECT_ALL_REVIEWS_BY_EMPLOYEE, (id,))
        return map(lambda review: Review(review[0], review[1], review[2], review[3], 
            review[4], review[5], review[6], review[7], review[8], 
            review[9], review[10], review[11], review[12]), reviews)

    def get_tl_required_reviews(self):
        reviews = self.repository.execute_query(SELECT_TL_REQUIRED_REVIEWS)
        return map(lambda review: Review(review[0], review[1], review[2], review[3], 
            review[4], review[5], review[6], review[7], review[8], 
            review[9], review[10], review[11], review[12]), reviews) 

    def get_all_employees(self):
        employees = self.repository.execute_query(SELECT_ALL_EMPLOYEES)
        return map(lambda employee: Employee(employee[0], employee[1], employee[2], employee[3], employee[4]), employees)

    def get_employee_by_id(self, employee_id):
        employee = self.repository.execute_query(SELECT_EMPLOYEE_BY_ID, (employee_id,))[0]
        return Employee(employee[0], employee[1], employee[2], employee[3], employee[4])

    def set_tl_assistance_by_id(self, tl_assistance_required, checked_out_user, review_id):
        self.repository.execute_command(SET_TL_ASSISTANCE_REQUIRED_BY_ID, (tl_assistance_required, checked_out_user, review_id))

    def set_close_or_check(self, status, review_id):
        self.repository.execute_command(SET_CLOSE_OR_MANUAL_CHECK_BY_ID, (status, review_id))

    def clear_checked_out_user(self, review_id):
        self.repository.execute_command(CLEAR_CHECKED_OUT_USER_BY_ID, (review_id,))

    def add_response(self, response):
        result = self.repository.execute_command(ADD_RESPONSE, (response.get_body(), response.get_coupon_id(), response.get_employee_id(), response.get_review_id()))
        return result

    def set_review_checked_out(self, status, review_id, employee_id):
        self.repository.execute_command(SET_CHECKED_OUT_BY_ID, (status, review_id, employee_id))

    def add_coupon(self, coupon):
        self.repository.execute_command(ADD_COUPON_INITIAL, (coupon.get_code(), coupon.get_type(), coupon.get_value()))

    def update_coupon(self, coupon_code, response_id):
        self.repository.execute_command(UPDATE_COUPON_WITH_RESPONSE_ID, (response_id, coupon_code))

    def add_template(self, template):
        self.repository.execute_command(ADD_TEMPLATE, (template.get_title(), template.get_body(), template.get_last_edited_user_id())) 

    def get_template_titles(self):
        titles = self.repository.execute_query(SELECT_ALL_TEMPLATE_TITLES)
        return map(lambda title : title[0], titles)

    def get_template_by_title(self, template_title):
        template = self.repository.execute_query(SELECT_TEMPLATE_BY_TITLE, (template_title,))[0]
        return Template(template[1], template[2], template[3], template[0])

    def update_template(self, template_body, last_edited_user_id, template_title):
        self.repository.execute_command(UPDATE_TEMPLATE, (template_body, last_edited_user_id, template_title))

    def get_customer_by_id(self, customer_id):
        customer = self.repository.execute_query(SELECT_CUSTOMER_BY_ID, (customer_id,))[0]
        return Customer(customer[0], customer[1], customer[2], customer[3], customer[4])

    def send_email(self, review, response, customer):
        msg = "Dear " + customer.get_name() + ",\n\n" \
        + "We are grateful that you took the time out to leave us a review. Your feedback helps us to improve service for everyone. We have shared this with the team to let them know how we are doing. " \
        + "\n Our customer service representative has responded." \
        + "\n\n Your review:\n\n\n" \
        + review \
        + "\n\n Our response:\n\n\n" \
        + response.get_body()

        self.__fire_and_forget(lambda: self.mail.send_mail(msg, customer.get_email()))

    def get_null_importance_reviews(self):
        reviews = self.repository.execute_query(SELECT_ALL_REVIEWS_WHERE_IMPORTANCE_SCORE_IS_NULL)
        return map(lambda review: CustomerReview(review[0], review[1], review[2], review[3]), reviews)

    def update_importance_scores(self, importance_score, review_id):
        self.repository.execute_command(UPDATE_IMPORTANCE_SCORE, (importance_score, review_id))

    def __fire_and_forget(self, task, *args, **kwargs):
        loop = asyncio.get_event_loop()
        if callable(task):
            return loop.run_in_executor(None, task, *args, **kwargs)
        else:    
            raise TypeError('Task must be a callable')


 
