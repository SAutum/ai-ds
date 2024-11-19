def get_query() -> str:
    # BEGIN_SOLUTION

    return """
    SELECT
        customer.id,
        customer.firstname,
        customer.lastname
    FROM
        customer
    WHERE
        NOT EXISTS (
            SELECT
                *
            FROM
                purchase
                JOIN product ON
                    purchase.product_id = product.id
            WHERE
                product.productname = 'Pizza' AND
                purchase.customer_id = customer.id
        )
    ORDER BY
        customer.lastname DESC
    """

    # Alternative solution
    return """
    SELECT
        customer.*
    FROM
        customer
    EXCEPT
    SELECT
        customer.*
    FROM
        customer, product, purchase
    WHERE
        purchase.product_id = product.id AND
        purchase.customer_id = customer.id AND
        productname = 'Pizza'
    ORDER BY
        customer.lastname DESC
    """

    # END_SOLUTION

    # This query is just a placeholder.
    return "SELECT attribute FROM relation"
