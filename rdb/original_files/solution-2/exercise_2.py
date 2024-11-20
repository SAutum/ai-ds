import sqlite3


def create_database() -> None:
    # BEGIN_SOLUTION

    with sqlite3.connect("mydatabase.db") as db:
        cursor = db.cursor()

        # Create table
        cursor.execute(
            """
            CREATE TABLE
                primenumbers
            (
                id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                value INTEGER
            )
        """
        )

        n = 7920
        is_prime = [{0: 0, 1: 0, 2: 1}.get(i, i % 2) for i in range(n)]
        for step in range(3, n, 2):
            for j in range(step * 2, n, step):
                is_prime[j] = False

        primenumbers = [(i,) for i in range(n) if is_prime[i]]

        cursor.executemany("INSERT INTO primenumbers (value) VALUES (?)", primenumbers)

    # END_SOLUTION
