SELECT_ALL_REVIEWS = "SELECT * FROM review_clone_test"

SELECT_ALL_USERS = "SELECT * FROM users"

SELECT_ALL_EMPLOYEES = "SELECT * FROM employee"

SELECT_EMPLOYEE_BY_ID = "SELECT * FROM employee WHERE id = %s"

SELECT_ALL_TEST_REVIEWS = "SELECT * FROM review_clone_test"

SELECT_NEXT_REVIEW = "SELECT * FROM review_clone_test WHERE status = 'NEW' AND tl_assistance_required IS null ORDER BY importance_score desc LIMIT 1"

SELECT_REVIEWS = "SELECT * FROM review_clone_test ORDER BY importance_score desc LIMIT %s"

SELECT_REVIEW_BY_ID = "SELECT * FROM review_clone_test WHERE id = %s"

UPDATE_STATUS = "ALTER TABLE review_clone_test set status = 'closed' where id = %s"

CALC_IMPORTANCE_VALUES = "SELECT r.star_rating, c.premier FROM review_clone_test r INNER JOIN customer c where c.id = r.customer_id"