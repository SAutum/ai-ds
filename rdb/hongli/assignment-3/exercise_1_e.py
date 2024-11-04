def get_query() -> str:
    # Your solution goes here.
    customer_amount = "SELECT customer_id, SUM(amount) AS total_amount \
                FROM purchase GROUP BY customer_id"
    # Question: sql style placeholder here?
    return "SELECT * FROM ({}) \
                WHERE total_amount = (SELECT MIN(total_amount) FROM ({}))"\
                    .format(customer_amount, customer_amount)
