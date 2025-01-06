def create_index_and_stuff() -> str:
    # Your solution goes here.

    return """

    CREATE INDEX index_pixel_xy ON pixel (((x - 174)^2 + (y - 50)^2));

    """


def get_query() -> str:
    # Your solution goes here.
    # You may modify this query, but it must return the same pixels.

    return """
    SELECT r, g, b, x, y
    FROM
        pixel
    WHERE
        (x - 174)^2 + (y - 50)^2 BETWEEN %s^2 AND %s^2
    """
