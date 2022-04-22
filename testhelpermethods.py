import unittest
from Presentation.helpermethods import calculate_importance_score, validate_coupon_amount
from Persistence.Entities.customerreview import CustomerReview

class TestHelperMethods(unittest.TestCase):

    #validate_coupon_amount tests
    def test_validate_coupon_amount_tl_happy_flow(self):
        expectedCouponLength = 10
        amount = '20'
        isTl = 1
        isPremierCustomer = 1
        actual = validate_coupon_amount(amount, isTl, isPremierCustomer)
        self.assertEqual(len(actual), expectedCouponLength)

    def test_validate_coupon_amount_csr_happy_flow(self):
        expectedCouponLength = 10
        amount = '10'
        isTl = 0
        isPremierCustomer = 1
        actual = validate_coupon_amount(amount, isTl, isPremierCustomer)
        self.assertEqual(len(actual), expectedCouponLength)

    def test_validate_coupon_amount_tl_exceeds_allowed_amount(self):
        expectedMessage = 'The max coupon value available is £25'
        amount = '70'
        isTl = 1
        isPremierCustomer = 0
        try:
            validate_coupon_amount(amount, isTl, isPremierCustomer)
        except Exception as e:
            self.assertEqual(str(e), expectedMessage)

    def test_validate_coupon_amount_csr_exceeds_allowed_amount(self):
        expectedMessage = 'The max coupon value available is £10'
        amount = '40'
        isTl = 0
        isPremierCustomer = 0
        try:
            validate_coupon_amount(amount, isTl, isPremierCustomer)
        except Exception as e:
            self.assertEqual(str(e), expectedMessage)

    
    #calculate_importance_score tests    
    def test_calculate_importance_score_for_2_star_review(self):
        customerReview = CustomerReview(4, 2, 0, "Terrible product!")
        sentimentScore = -1
        actual = calculate_importance_score(customerReview, sentimentScore)
        expected = 4
        self.assertEqual(actual, expected)

    def test_calculate_importance_score_for_5_star_review(self):
        customerReview = CustomerReview(7, 5, 1, "Fantastic Product!")
        sentimentScore = 2
        actual = calculate_importance_score(customerReview, sentimentScore)
        expected = 2
        self.assertEqual(actual, expected)

if __name__ == '__main__':
    unittest.main()
