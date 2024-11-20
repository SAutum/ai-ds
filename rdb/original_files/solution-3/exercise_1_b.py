def get_query() -> str:
    # BEGIN_SOLUTION

    return """
    SELECT
        'Hello, ' || firstname || ' ' || lastname
        AS greeting
    FROM
        customer
    WHERE
        lastname ILIKE '%W%'
    """

    # Alternative solution with CONCAT instead of '||' operator
    # and UPPER(...) LIKE instead of ILIKE.
    """
    SELECT
        CONCAT('Hello, ', firstname, ' ', lastname)
        AS greeting
    FROM
        customer
    WHERE
        UPPER(lastname) LIKE '%W%'
    """

    # END_SOLUTION

    # This is just a placeholder.
    return "SELECT duck FROM pond"
