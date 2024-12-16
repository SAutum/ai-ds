import re
import zipme
import random
import psycopg
import datetime
import statistics
from collections import defaultdict
from exercise_1_c import get_query


def test(count: int) -> None:
    random.seed(count)

    query = get_query()

    overs = list(re.findall(r"\bOVER\b", query, re.IGNORECASE))

    assert len(overs) >= 1, "Your query should contain the OVER keyword"

    with psycopg.connect() as conn:
        with conn.cursor() as cursor:

            cursor.execute("DROP TABLE IF EXISTS snowfall")
            cursor.execute("CREATE TABLE snowfall (sid BIGSERIAL PRIMARY KEY, date DATE, snow REAL)")

            start_year = random.randint(2000, 2020)
            start_month = random.randint(1, 12)
            start_day = random.randint(1, 28)
            date = datetime.date(start_year, start_month, start_day)

            snow_per_year_per_month = defaultdict(lambda: defaultdict(list))
            snow_per_year_per_week = defaultdict(lambda: defaultdict(list))
            snow_per_year = defaultdict(list)

            data = []
            for _ in range(count):
                snow = random.randrange(100)

                month = date.month
                year = date.year
                week = date.isocalendar()[1]

                snow_per_year_per_month[year][month].append(snow)
                snow_per_year_per_week[year][week].append(snow)
                snow_per_year[year].append(snow)

                data.append((date, snow))
                date = date + datetime.timedelta(days=1)

            cursor.executemany("INSERT INTO snowfall (date, snow) VALUES (%s, %s)", data)

            cursor.execute(query)

            results = cursor.fetchall()

            assert isinstance(results, list)

            attributes = [desc[0] for desc in cursor.description]

            expected_attributes = ["date", "avg_week", "avg_month"]

            assert attributes == expected_attributes, f"Expected attributes {expected_attributes}, but got {attributes}"

            table = {}
            for date, avg_week, avg_month in results:
                date = date.isoformat()
                table[date] = (avg_week, avg_month)

            for date, _ in data:
                week = date.isocalendar()[1]
                month = date.month
                year = date.year
                date = date.isoformat()

                expected_avg_month = statistics.mean(snow_per_year_per_month[year][month])
                expected_avg_week = statistics.mean(snow_per_year_per_week[year][week])

                your_avg_month = table[date][1]

                tolerance = 1e-5

                assert (
                    abs(expected_avg_month - your_avg_month) < tolerance
                ), f"Expected avg_month {expected_avg_month} for date {date}, but got {your_avg_month}"
                assert (
                    abs(expected_avg_week - table[date][0]) < tolerance
                ), f"Expected avg_week {expected_avg_week} for date {date}, but got {table[date][0]}"


if __name__ == "__main__":
    for count in [10, 100, 300, 500, 1000]:
        test(count)
    zipme.finish(__file__)

# 37167375443200000000
