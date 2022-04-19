SELECT_TL_REQUIRED_REVIEWS = "SELECT * FROM review_clone_test WHERE tl_assistance_required = 1"

SELECT_ALL_EMPLOYEES = "SELECT * FROM employee"

SELECT_EMPLOYEE_BY_ID = "SELECT * FROM employee WHERE id = %s"

SELECT_ACTIVE_REVIEWS = "SELECT * FROM review_clone_test WHERE status != 'CLOSED' ORDER BY importance_score desc"

SELECT_ALL_REVIEWS_BY_EMPLOYEE = "SELECT * FROM review_clone_test WHERE checked_out_user = %s"

SELECT_NEXT_REVIEW = "SELECT * FROM review_clone_test WHERE status = 'NEW' AND tl_assistance_required IS null ORDER BY importance_score desc LIMIT 1"

SELECT_REVIEW_BY_ID = "SELECT * FROM review_clone_test WHERE id = %s"

SELECT_CUSTOMER_BY_ID = "SELECT * FROM customer WHERE id = %s"

UPDATE_STATUS = "ALTER TABLE review_clone_test set status = 'closed' where id = %s"

CALC_IMPORTANCE_VALUES = "SELECT r.star_rating, c.premier FROM review_clone_test r INNER JOIN customer c where c.id = r.customer_id"

SELECT_RESPONSE_ID_BY_REVIEW_ID = "SELECT id FROM response WHERE review_id = %s"

GET_COUPON_ID_WITH_COUPON_CODE = "SELECT id FROM coupon WHERE coupon_code = %s"

SELECT_ALL_TEMPLATE_TITLES = "SELECT title FROM template"

SELECT_TEMPLATE_BY_TITLE = "SELECT * FROM template WHERE title = %s"

SELECT_ALL_REVIEWS_WHERE_IMPORTANCE_SCORE_IS_NULL = "SELECT r.id, r.star_rating, cu.premier, r.body FROM review_clone_test r inner join customer cu WHERE r.customer_id = cu.id AND r.importance_score IS NULL"