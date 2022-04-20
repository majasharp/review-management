SET_TL_ASSISTANCE_REQUIRED_BY_ID = "UPDATE review_clone_test SET tl_assistance_required = %s, checked_out_user = %s WHERE id = %s"

ADD_RESPONSE = "INSERT INTO response (body, coupon_id, employee_id, review_id) VALUES(%s, %s, %s, %s)"

SET_CHECKED_OUT_BY_ID = "UPDATE review_clone_test SET status = %s, checked_out_user = %s WHERE id = %s"

SET_CLOSE_OR_MANUAL_CHECK_BY_ID = "UPDATE review_clone_test SET status = %s WHERE id = %s"

ADD_COUPON_INITIAL = "INSERT INTO coupon (coupon_code, coupon_type, coupon_value) VALUES (%s, %s, %s)"

UPDATE_COUPON_WITH_RESPONSE_ID = "UPDATE coupon SET response_id = %s WHERE coupon_code = %s"

ADD_TEMPLATE = "INSERT INTO template (title, body, last_edited_user_id) VALUES (%s, %s, %s)"

UPDATE_TEMPLATE = "UPDATE template SET body = %s, last_edited_user_id = %s WHERE title = %s"

UPDATE_IMPORTANCE_SCORE = "UPDATE review_clone_test SET importance_score = (%s) WHERE id = (%s)"

CLEAR_CHECKED_OUT_USER_BY_ID = "UPDATE review_clone_test SET checked_out_user = null where id = %s"