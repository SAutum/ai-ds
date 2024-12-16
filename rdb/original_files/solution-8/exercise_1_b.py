def filter_outliers(filename: str) -> list[tuple[float, float]]:
    # BEGIN_SOLUTION
    with psycopg.connect() as connection:
        with connection.cursor() as cursor:
            cursor.execute("DROP TABLE IF EXISTS waterlevel")
            cursor.execute("CREATE TABLE waterlevel (ti DOUBLE PRECISION, yi DOUBLE PRECISION)")
            with open(filename, encoding="utf-8") as f:
                text = f.read()
            with cursor.copy("COPY waterlevel FROM STDIN WITH CSV HEADER") as copy:
                copy.write(text)
            cursor.execute("""
            SELECT
                ti,
                CASE WHEN
                    ABS(yi - AVG(yi) OVER (ROWS BETWEEN 10 PRECEDING AND 10 FOLLOWING)) >= 0.5
                THEN
                    (SUM(yi) OVER (ROWS BETWEEN 1 PRECEDING AND 1 FOLLOWING) - yi) / 2
                ELSE
                    yi
                END
            FROM waterlevel
            """)

            return cursor.fetchall()


import psycopg

# END_SOLUTION
