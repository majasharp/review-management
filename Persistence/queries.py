SELECT_ALL_REVIEWS = "SELECT * FROM review where id = 1"

SELECT_ALL_USERS = "SELECT * FROM users"

SELECT_ALL_TEST_REVIEWS = "SELECT * FROM review_clone_test"

SELECT_NEXT_REVIEW = "SELECT * FROM review_clone_test WHERE status = 'NEW' ORDER BY importance_score desc LIMIT 1"

SELECT_REVIEWS = "SELECT * FROM review_clone_test ORDER BY importance_score desc LIMIT %s"