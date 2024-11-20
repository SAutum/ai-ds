def get_query() -> str:
    # Your solution goes here.

    # This is just a placeholder.
    return "SELECT product_id, sum(amount) AS total_amount FROM purchase GROUP BY product_id Having sum(amount) >= 20"
