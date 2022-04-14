from Persistence.queries import *
from Persistence.commands import *
from Persistence.Entities.review import Review
from Persistence.Entities.employee import Employee
from Persistence.Entities.customer import Customer
from Persistence.Entities.template import Template

class Service:
    
    def __init__(self, repository):
        self.repository = repository

    def get_next_review(self):
        nextReview = self.repository.execute_query(SELECT_NEXT_REVIEW)[0]
        return Review(nextReview[0], nextReview[1], nextReview[2], nextReview[3], 
            nextReview[4], nextReview[5], nextReview[6], nextReview[7], nextReview[8], 
            nextReview[9], nextReview[10], nextReview[11], nextReview[12])

    def get_all_test_reviews(self):
        reviews = self.repository.execute_query(SELECT_ALL_TEST_REVIEWS)
        return map(lambda review: Review(review[0], review[1], review[2], review[3], 
            review[4], review[5], review[6], review[7], review[8], 
            review[9], review[10], review[11], review[12]), reviews)


    def get_specific_review(self, reviewID):
        review = self.repository.get_rows(SELECT_REVIEW_BY_ID, (reviewID,))
        return Review(review[0], review[1], review[2], review[3], 
            review[4], review[5], review[6], review[7], review[8], 
            review[9], review[10], review[11], review[12])

    def get_importance_calc_values(self):
        reviews = self.repository.execute_query(CALC_IMPORTANCE_VALUES)
        return map(lambda review: Review(review[0], review[1], review[2], review[3], 
            review[4], review[5], review[6], review[7], review[8], 
            review[9], review[10], review[11], review[12]), reviews)

    def get_all_employees(self):
        employees = self.repository.execute_query(SELECT_ALL_EMPLOYEES)
        return map(lambda employee: Employee(employee[0], employee[1], employee[2], employee[3], employee[4]), employees)

    def get_employee_by_id(self, employee_id):
        employee = self.repository.execute_query(SELECT_EMPLOYEE_BY_ID, (employee_id,))[0]
        return Employee(employee[0], employee[1], employee[2], employee[3], employee[4])

    def set_tl_assistance_by_id(self, tl_assistance_required, review_id):
        self.repository.execute_command(SET_TL_ASSISTANCE_REQUIRED_BY_ID, (tl_assistance_required, review_id))

    def add_response(self, response):
        return self.repository.execute_command(ADD_RESPONSE, (response.get_body(), response.get_coupon_id(), response.get_employee_id(), response.get_review_id()))

    def set_review_status(self, status, review_id, employee_id):
        self.repository.execute_command(SET_STATUS_BY_ID, (status, review_id, employee_id))

    def add_coupon(self, coupon):
        self.repository.execute_command(ADD_COUPON_INITIAL, (coupon.get_code(), coupon.get_type(), coupon.get_value()))

    def update_coupon(self, coupon_code, response_id):
        self.repository.execute_command(UPDATE_COUPON_WITH_RESPONSE_ID, (response_id, coupon_code))

    def get_coupon_id(self, code):
        self.repository.execute_query(GET_COUPON_ID_WITH_COUPON_CODE, (code,))

    def get_response_id(self, review_id):
        self.repository.execute_query(SELECT_RESPONSE_ID_BY_REVIEW_ID, (review_id,))

    def add_template(self, template):
        self.repository.execute_command(ADD_TEMPLATE, (template.get_title(), template.get_body(), template.get_last_edited_user_id())) 

    def get_template_titles(self):
        titles = self.repository.execute_query(SELECT_ALL_TEMPLATE_TITLES)
        return map(lambda title : title[0], titles)

    def get_template_by_title(self, template_title):
        template = self.repository.execute_query(SELECT_TEMPLATE_BY_TITLE, (template_title,))[0]
        return Template(template[1], template[2], template[3], template[0])

    def get_customer_by_id(self, customer_id):
        customer = self.repository.execute_query(SELECT_CUSTOMER_BY_ID, (customer_id,))[0]
        return Customer(customer[0], customer[1], customer[2], customer[3], customer[4])