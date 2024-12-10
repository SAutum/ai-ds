def get_query() -> str:

    # remember to extract year also
    query = """
                SELECT date,
                    AVG(snow)
                        OVER(PARTITION BY EXTRACT(YEAR FROM date),
                            EXTRACT(WEEK FROM date))
                        AS avg_week,
                    AVG(snow)
                        OVER(PARTITION BY EXTRACT(YEAR FROM date),
                            EXTRACT(MONTH FROM date))
                        AS avg_month
                FROM snowfall
            """

    return query
