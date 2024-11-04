def get_query() -> str:
    # Your solution goes here.

    # This is just a placeholder.
    return "SELECT * FROM (SELECT product_id, SUM(amount) \
                            AS total_amount \
                            FROM purchase GROUP BY product_id)\
            WHERE total_amount >= 20"
