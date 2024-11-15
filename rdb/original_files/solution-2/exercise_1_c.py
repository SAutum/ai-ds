def get_query() -> str:
    # BEGIN_SOLUTION

    return """
    SELECT
        COUNT(DISTINCT productname)
    FROM
        product
    """

    # END_SOLUTION

    # This query is just a placeholder.
    return "SELECT attribute FROM relation"
