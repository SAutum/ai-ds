def get_query() -> str:
    # BEGIN_SOLUTION

    return """
    SELECT
        customer_id AS customer_id,
        SUM(amount * price) AS total_money_spent
    FROM
        purchase
        JOIN product ON purchase.product_id = product.product_id
    GROUP BY
        customer_id
    ORDER BY
        total_money_spent DESC
    LIMIT 1
    """

    # Alternatively, use
    # FETCH FIRST 1 ROWS ONLY
    # instead of
    # LIMIT 1
    # if your database strictly follows SQL standard.

    # END_SOLUTION

    # This is just a placeholder.
    return "SELECT attribute FROM relation"
