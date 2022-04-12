from turtle import update


SET_TL_ASSISTANCE_REQUIRED_BY_ID = "UPDATE review_clone_test SET tl_assistance_required = %s WHERE id = %s"

ADD_RESPONSE = "INSERT INTO response (body, coupon_id, employee_id, review_id) VALUES(%s, %s, %s, %s)"

SET_STATUS_BY_ID = "UPDATE review_clone_test SET status = %s, checked_out_user = %s WHERE id = %s"

ADD_COUPON_INITIAL = "INSERT INTO coupon (coupon_code, coupon_type, coupon_value) VALUES (%s, 'pound', %s)"

UPDATE_COUPON_WITH_RESPONSEID = "UPDATE coupon SET response_id = %s WHERE id = %s"

ADD_TEMPLATE = "INSERT INTO template (body, last_edited_user_id) VALUES (%s, %s)"

