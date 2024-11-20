def get_query() -> str:
    # BEGIN_SOLUTION

    return """
    SELECT
        id, firstname, lastname
    FROM
        customer
    WHERE
        lastname LIKE 'Sch%'
    """

    # END_SOLUTION

    # This query is just a placeholder.
    return "SELECT attribute FROM relation"
