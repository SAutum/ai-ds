def get_query() -> str:

    query = """
    SELECT A, B, C, D, E, F, G FROM mytable GROUP BY
        CUBE(B),
        ROLLUP(D, C, A),
        GROUPING SETS((E), (E, F), (F, G), (G))
    """
    # 8 = 4 * 2
    # 4 from rollup and 2 from cube

    return query
