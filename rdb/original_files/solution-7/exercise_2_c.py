def get_query() -> str:
    # Remember to start a PostgreSQL database and run test_populate_database.py
    # from the previous assignment to fill the database before you run the tests.

    # BEGIN_SOLUTION

    query = """
    SELECT
        NULL AS category, NULL AS subcategory, year, COUNT(*) AS n
    FROM
        sale
        JOIN product ON sale.product_id = product.product_id
        JOIN timestamp ON sale.timestamp_id = timestamp.timestamp_id
    GROUP BY
        (year)
UNION ALL
    SELECT
        category, NULL AS subcategory, year, COUNT(*) AS n
    FROM
        sale
        JOIN product ON sale.product_id = product.product_id
        JOIN timestamp ON sale.timestamp_id = timestamp.timestamp_id
    GROUP BY
                (year, category)
UNION ALL
    SELECT
        category, NULL AS subcategory, NULL AS year, COUNT(*) AS n
    FROM
        sale
        JOIN product ON sale.product_id = product.product_id
        JOIN timestamp ON sale.timestamp_id = timestamp.timestamp_id
    GROUP BY
                (category)
UNION ALL
    SELECT
        category, subcategory, NULL AS year, COUNT(*) AS n
    FROM
        sale
        JOIN product ON sale.product_id = product.product_id
        JOIN timestamp ON sale.timestamp_id = timestamp.timestamp_id
    GROUP BY
                (category, subcategory)
UNION ALL
    SELECT
        category, subcategory, year, COUNT(*) AS n
    FROM
        sale
        JOIN product ON sale.product_id = product.product_id
        JOIN timestamp ON sale.timestamp_id = timestamp.timestamp_id
    GROUP BY
                (year, category, subcategory)
UNION ALL
    SELECT
        NULL AS category, NULL AS subcategory, NULL AS year, COUNT(*) AS n
    FROM
        sale
        JOIN product ON sale.product_id = product.product_id
        JOIN timestamp ON sale.timestamp_id = timestamp.timestamp_id
    """
    # END_SOLUTION

    return query
