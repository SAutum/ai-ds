def get_query() -> str:
    # BEGIN_SOLUTION
    query = """
    SELECT
        date,
        AVG(snow) OVER (PARTITION BY EXTRACT(WEEK FROM date), EXTRACT(YEAR FROM date)) AS avg_week,
        AVG(snow) OVER (PARTITION BY EXTRACT(MONTH FROM date), EXTRACT(YEAR FROM date)) AS avg_month
    FROM snowfall
    """
    # END_SOLUTION

    return query
