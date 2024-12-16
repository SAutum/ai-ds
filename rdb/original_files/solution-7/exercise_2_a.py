def get_query() -> str:
    # Remember to start a PostgreSQL database and run test_populate_database.py
    # from the previous assignment to fill the database before you run the tests.

    # BEGIN_SOLUTION

    # When using CUBE(year, category, subcategory), the invalid attribute
    # combinations (year, subcategory) and (subcategory) arise. Aggregating
    # over subcategories from different categories does not make sense.
    # For example, we might be adding sales of the subcategory "Bat" of the
    # "Animal" category with sales of the subcategory "Bat" (baseball bat)
    # of the "Sports" category, which do not have much in common.
    # We have to exclude this combination, which can be done by splitting the
    # CUBE into a CUBE and a ROLLUP.

    query = """
    SELECT
        category, subcategory, year, COUNT(*) AS n
    FROM
        sale
        JOIN product ON sale.product_id = product.product_id
        JOIN timestamp ON sale.timestamp_id = timestamp.timestamp_id
    GROUP BY
        CUBE(year),
        ROLLUP(category, subcategory)
    """

    # END_SOLUTION

    return query
