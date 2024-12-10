import psycopg


def create_database(cursor) -> None:
    # Create data for database here. Make sure to drop existing tables
    # when this code is called multiple times with DROP TABLE IF EXISTS ...
    cursor.execute('DROP TABLE IF EXISTS sale CASCADE')
    cursor.execute('DROP TABLE IF EXISTS company CASCADE')

    # create two tables
    cursor.execute("""
                    CREATE TABLE company (
                        company_id BIGSERIAL PRIMARY KEY,
                        company_name TEXT,
                        country TEXT
                    )
                    """)

    cursor.execute("""
                    CREATE TABLE sale (
                        product_id BIGSERIAL PRIMARY KEY,
                        company_id BIGSERIAL REFERENCES company(company_id),
                        product_name TEXT,
                        product_category TEXT,
                        price DOUBLE PRECISION
                    )
                    """)

    # add 1000 tuples to company table
    for i in range(1000):
        tup = ("company_{}".format(i), "country_{}".format(i//7))
        cursor.execute("""
                            INSERT INTO company
                                (company_name, country)
                            VALUES
                                (%s, %s)
                        """, tup)

    # add 200 tuples to product table
    for i in range(100):
        tup = (i//50 + 1, i, "category_{}".format(i//100), i//7 * 3.14159)
        cursor.execute("""INSERT INTO sale
                            (company_id, product_name, product_category, price)
                        VALUES (%s, %s, %s, %s)""", tup)

        tup = (i//100 + 1, i, "category_{}".format(i//5), i//7 * 3.14159)
        cursor.execute("""INSERT INTO sale
                            (company_id, product_name, product_category, price)
                        VALUES (%s, %s, %s, %s)""", tup)


def get_query1() -> str:
    # This is the first query without early grouping.
    query = """
                SELECT
                    product_category, company_name, ROUND(SUM(price)::NUMERIC,2)
                FROM
                    sale, company
                GROUP BY
                    product_category, company.company_name
                ORDER BY
                    company_name, product_category
            """

    return query


def get_query2() -> str:
    # This is the second query with early grouping.
    # Both queries should ALWAYS return the same results, even if the data
    # in the database changes!
    query = """
                SELECT
                    product_category, company_name, ROUND(SUM(price)::NUMERIC,2)
                FROM
                    (SELECT
                        product_category, SUM(price) AS price, company_id
                    FROM
                        sale
                    GROUP BY
                        product_category, company_id
                    ), company
                GROUP BY
                    product_category, company_name
                ORDER BY
                    company_name, product_category
            """
    # Your solution goes here.

    return query
