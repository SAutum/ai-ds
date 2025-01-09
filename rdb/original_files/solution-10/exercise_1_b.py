def create_index_and_stuff() -> str:
    # BEGIN_SOLUTION

    # By far the easiest solution is to create a functional index ont he distance:
    # CREATE INDEX squared_distance_index ON pixel (((x - 174)^2 + (y - 50)^2))
    # https://www.postgresql.org/docs/7.3/indexes-functional.html
    # However, some databases do not support functional indexes.
    # Here is an alternative solution which precomputes distances to the center.

    return """
    CREATE INDEX index_1b ON pixel (((x - 174)^2 + (y - 50)^2));
    """

    # Alternative solution with index on precomputed distance
    # return """
    # ALTER TABLE pixel ADD distance DOUBLE PRECISION;
    # CREATE INDEX index_1b ON pixel USING BTREE (distance);
    # UPDATE pixel SET distance = ((x - 174)^2 + (y - 50)^2)^0.5;
    # """

    # END_SOLUTION

    return """

    You may create an index or do other things here.
    You can execute multiple statements; this is done with semicolons.

    """


def get_query() -> str:
    # BEGIN_SOLUTION

    # Alternative solution with precomputed distance
    # return """
    # SELECT r, g, b, x, y FROM pixel WHERE %s <= distance AND distance <= %s
    # """

    # END_SOLUTION

    # You may modify this query, but it must return the same pixels.

    return """
    SELECT r, g, b, x, y FROM pixel WHERE
        (x - 174)^2 + (y - 50)^2 BETWEEN %s^2 AND %s^2
    """
