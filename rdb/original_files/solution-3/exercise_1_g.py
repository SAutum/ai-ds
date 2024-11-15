def get_query() -> str:
    # BEGIN_SOLUTION

    return """
    DELETE FROM
        customer
    WHERE
        firstname = 'Test' AND lastname = 'Customer'
    """

    # END_SOLUTION

    # This is just a placeholder.
    return "SELECT attribute FROM relation"
