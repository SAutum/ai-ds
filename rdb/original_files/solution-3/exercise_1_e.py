def get_query() -> str:
    # BEGIN_SOLUTION

    return """
    SELECT
        customer_id AS customer_id,
        SUM(amount) AS total_amount
    FROM
        purchase
    GROUP BY
        customer_id
    HAVING
        SUM(amount) IN (
            SELECT
                SUM(amount) AS total_amount
            FROM
                purchase
            GROUP BY
                customer_id
            ORDER BY
                total_amount ASC
            LIMIT 1
        )
    """

    # Alternative solution using so-called "CTE" (Common Table Expression)

    """
    WITH customer_totals AS (
        SELECT
            customer_id,
            SUM(purchase.amount) AS total_amount
        FROM
            purchase
        GROUP BY
            customer_id
    )
    SELECT * FROM
        customer_totals
    WHERE
        total_amount = (
            SELECT
                MIN(total_amount)
            FROM
                customer_totals
        )
    """

    # using FETCH FIRST 1 ROWS WITH TIES
    """
    SELECT
        customer_id AS customer_id,
        SUM(amount) AS total_amount
    FROM
        purchase
    GROUP BY
        customer_id
    ORDER BY
        total_amount
    FETCH FIRST 1 ROWS WITH TIES
    """

    # END_SOLUTION

    # This is just a placeholder.
    return "SELECT attribute FROM relation"
