def get_query() -> str:
    # Remember to start a PostgreSQL database and run test_populate_database.py
    # from the previous assignment to fill the database before you run the tests.

    # Your solution goes here.
    query = """ SELECT
                    category, subcategory, year, COUNT(*) AS n
                FROM
                    sale
                    JOIN product ON sale.product_id = product.product_id
                    JOIN timestamp ON sale.timestamp_id = timestamp.timestamp_id
                GROUP BY
                   GROUPING SETS((category,subcategory),(category),()),
                   GROUPING SETS((year),());"""
    return query
