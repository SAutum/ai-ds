def get_query() -> str:
    # Your solution goes here.

    # ILIKE: case: insensitive
    # This is just a placeholder.
    return "SELECT 'Hello, '||firstname||' '||lastname AS greeting \
            FROM customer \
            WHERE (lastname LIKE '%w%') OR (lastname LIKE '%W%')"
