def get_query() -> str:
    # BEGIN_SOLUTION

    return """
    SELECT
        customer.id, firstname, lastname
    FROM
        customer
        JOIN purchase ON
            purchase.customer_id = customer.id
    GROUP BY
        customer.id, firstname, lastname
    HAVING
        COUNT(*) = 5
        AND SUM(purchase.amount) >= 28;
    """

    # END_SOLUTION

    # This query is just a placeholder.
    return "SELECT attribute FROM relation"
