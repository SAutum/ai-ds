def get_query() -> str:
    # BEGIN_SOLUTION

    return """
    UPDATE
        customer
    SET
        lastname = 'Smith'
    WHERE
        lastname IS NULL
    """

    # END_SOLUTION

    # This is just a placeholder.
    return "SELECT attribute FROM relation"
