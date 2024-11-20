def get_query() -> str:
    # BEGIN_SOLUTION

    return """
    SELECT
        product_id,
        SUM(amount) AS total_amount
    FROM
        purchase
    GROUP BY
        product_id
    HAVING
        SUM(amount) >= 20
    """

    # Alternative solution with subquery if you do not know the HAVING keyword
    """
    SELECT * FROM (
        SELECT
            product_id,
            SUM(amount) as total_amount
        FROM
            purchase
        GROUP BY
            product_id
    )
    WHERE
        total_amount >= 20
    """

    # END_SOLUTION

    # This is just a placeholder.
    return "SELECT money FROM bank WHERE security = 'weak'"
