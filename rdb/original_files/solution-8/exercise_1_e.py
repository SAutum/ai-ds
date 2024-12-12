import psycopg


def create_database(cursor) -> None:
    # Create data for database here. Make sure to drop existing tables
    # when this code is called multiple times with DROP TABLE IF EXISTS ...

    # BEGIN_SOLUTION
    import random
    from decimal import Decimal

    random.seed(0)

    cursor.execute("DROP TABLE IF EXISTS sale CASCADE")
    cursor.execute("DROP TABLE IF EXISTS timestamp CASCADE")
    cursor.execute("DROP TABLE IF EXISTS geography CASCADE")

    cursor.execute("""
    CREATE TABLE timestamp (
        timestamp_id INTEGER PRIMARY KEY,
        year INTEGER,
        month INTEGER,
        day INTEGER
    );

    CREATE TABLE geography (
        geography_id INTEGER PRIMARY KEY,
        city TEXT,
        state TEXT,
        country TEXT
    );

    CREATE TABLE sale (
        sale_id INTEGER PRIMARY KEY,
        timestamp_id INTEGER REFERENCES timestamp(timestamp_id),
        geography_id INTEGER REFERENCES geography(geography_id),
        price DECIMAL
    );
    """)

    geography = [
        (1, "New York", "NY", "USA"),
        (2, "Los Angeles", "CA", "USA"),
        (3, "Chicago", "IL", "USA"),
        (4, "Houston", "TX", "USA"),
        (5, "Philadelphia", "PA", "USA"),
    ]

    # generate a list of random timestamps between 2020-01-01 and 2021-12-31
    timestamp = []
    for timestamp_id in range(1, 1 + 1000):
        year = random.choice([2020, 2021])
        month = random.randint(1, 12)
        days_per_month = {2: 28, 4: 30, 6: 30, 9: 30, 11: 30}
        day = random.randint(1, days_per_month.get(month, 31))
        timestamp.append((timestamp_id, year, month, day))

    geography_ids = [geography_id for geography_id, _, _, _ in geography]
    timestamp_ids = [timestamp_id for timestamp_id, _, _, _ in timestamp]

    # generate a list of random sales
    sale = []
    for sale_id in range(1, 1 + 10000):
        timestamp_id = random.choice(timestamp_ids)
        geography_id = random.choice(geography_ids)
        price = Decimal(random.randint(1, 1000)) / Decimal(100)
        sale.append((sale_id, timestamp_id, geography_id, price))

    cursor.executemany("INSERT INTO geography VALUES (%s, %s, %s, %s)", geography)
    cursor.executemany("INSERT INTO timestamp VALUES (%s, %s, %s, %s)", timestamp)
    cursor.executemany("INSERT INTO sale VALUES (%s, %s, %s, %s)", sale)
    # END_SOLUTION


def get_query1() -> str:
    # This is the first query without early grouping.

    # BEGIN_SOLUTION

    query = """
    SELECT
        year,
        city,
        SUM(price) AS total_revenue,
        COUNT(*) AS total_count
    FROM
        sale,
        timestamp,
        geography
    WHERE
        sale.timestamp_id = timestamp.timestamp_id AND
        sale.geography_id = geography.geography_id
    GROUP BY
        year, city
    """

    # END_SOLUTION

    return query


def get_query2() -> str:
    # This is the second query with early grouping.
    # Both queries should ALWAYS return the same results, even if the data
    # in the database changes!

    # BEGIN_SOLUTION

    query = """
    SELECT
        year,
        city,
        SUM(subquery_revenue) AS total_revenue,
        SUM(subquery_count) AS total_count
    FROM
        (
            SELECT
                year,
                geography_id,
                SUM(price) AS subquery_revenue,
                COUNT(*) AS subquery_count
            FROM
                sale
            JOIN
                timestamp
            ON
                sale.timestamp_id = timestamp.timestamp_id
            GROUP BY
                year, geography_id
        ) AS subquery
    JOIN
        geography
    ON
        subquery.geography_id = geography.geography_id
    GROUP BY
        year, city
    """

    # END_SOLUTION

    return query
