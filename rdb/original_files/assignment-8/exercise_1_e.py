import psycopg


def create_database(cursor) -> None:
    # Create data for database here. Make sure to drop existing tables
    # when this code is called multiple times with DROP TABLE IF EXISTS ...

    # Your solution goes here.


def get_query1() -> str:
    # This is the first query without early grouping.

    # Your solution goes here.

    return query


def get_query2() -> str:
    # This is the second query with early grouping.
    # Both queries should ALWAYS return the same results, even if the data
    # in the database changes!

    # Your solution goes here.

    return query
