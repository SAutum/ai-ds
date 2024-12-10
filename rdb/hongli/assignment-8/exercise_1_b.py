import psycopg


def filter_outliers(filename: str) -> list[tuple[float, float]]:
    with psycopg.connect() as conn:
        with conn.cursor() as cursor:

            # create a database with table measurements
            cursor.execute('DROP TABLE IF EXISTS measurements CASCADE')
            # double precision for time is necessary!
            # otherwise: time will lose precision
            cursor.execute("""
                            CREATE TABLE measurements (
                                time_id BIGSERIAL PRIMARY KEY,
                                time DOUBLE PRECISION,
                                waterlevel DOUBLE PRECISION
                            )
                            """)

            with open(file=filename, encoding="utf-8") as f:
                text = f.read()

            with cursor.copy("""
                            COPY measurements (time, waterlevel)
                            FROM STDIN
                            WITH
                                CSV HEADER
                            """) as copy:
                copy.write(text)

            # query the outliers
            # I doubt exclude current row is a standard
            # https://modern-sql.com/caniuse/over_exclude_current_row
            cursor.execute("""
                            WITH outlier_detect AS (
                                SELECT
                                    time_id, waterlevel,
                                    AVG(waterlevel)
                                    OVER(ORDER BY time
                                        ROWS BETWEEN 10 PRECEDING AND
                                        10 FOLLOWING) AS threshold,
                                    AVG(waterlevel)
                                    OVER(ORDER BY time
                                        ROWS BETWEEN 1 PRECEDING AND
                                        1 FOLLOWING EXCLUDE CURRENT ROW)
                                    AS replacement
                                FROM measurements
                                )

                            UPDATE measurements
                                SET
                                    waterlevel =
                                    outlier_detect.replacement
                                FROM
                                    outlier_detect
                                WHERE
                                    measurements.time_id =
                                    outlier_detect.time_id
                                    AND
                                    ABS(outlier_detect.waterlevel -
                                    outlier_detect.threshold) > 0.5
                            """)

            cursor.execute("""
                            SELECT time, waterlevel
                            FROM measurements
                            ORDER BY time
                            """)

            results = []
            for tuple in cursor.fetchall():
                results.append(tuple)

    return results
