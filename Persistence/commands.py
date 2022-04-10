SET_TL_ASSISTANCE_REQUIRED_BY_ID = "UPDATE review_clone_test SET tl_assistance_required = %s WHERE id = %s"

ADD_RESPONSE = "INSERT INTO response (body, coupon_id, employee_id, review_id) VALUES(%s, %s, %s, %s)"

SET_STATUS_BY_ID = "UPDATE review_clone_test SET status = %s, checked_out_user = %s WHERE id = %s"