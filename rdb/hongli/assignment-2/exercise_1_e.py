def get_query() -> str:
    # Your solution goes here.

    # This query is just a placeholder.
    return "SELECT * FROM customer WHERE id IN \
        (SELECT customer_id FROM purchase GROUP BY customer_id \
            HAVING COUNT(id) = 5 AND SUM(amount) >= 28)"
