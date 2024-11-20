import sqlite3
import exercise_2
import os


def test() -> None:
    # Remove database file
    db_filename = "mydatabase.db"

    try:
        os.remove(db_filename)
    except FileNotFoundError:
        pass

    # Create new database
    exercise_2.create_database()

    # Check if database file has been created
    assert os.path.isfile(db_filename), f"Could not find file named {db_filename}"

    # Open database
    with sqlite3.connect(db_filename) as db:
        cursor = db.cursor()

        allowed_table_name_chars = set(
            "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_"
        )

        table_exists = False

        # Check all tables in database
        for table_info in cursor.execute("SELECT * FROM sqlite_master").fetchall():

            # Skip indexes and such
            if table_info[0] != "table":
                continue

            table_name = table_info[1]

            # Skip internal table
            if table_name == "sqlite_sequence":
                continue

            # WARNING!
            # Building queries using format strings is generally a source of
            # SQL injection vulnerabilities and should generally not be done,
            # so we ensure that the table name only consists of safe characters.
            assert all(c in allowed_table_name_chars for c in table_name)

            rows = cursor.execute(f"SELECT * FROM {table_name}").fetchall()

            print(f'The table "{table_name}" has {len(rows)} rows.')
            print("The first 10 rows are:")
            for row in rows[:10]:
                print(row)

            assert len(rows) == 1000, "Table must have 1000 rows of data!"

            assert len(rows[0]) >= 2, "Table must have at least 2 columns!"

            table_exists = True

    db.close()

    assert table_exists, "Could not find table with 1000 rows of data"

    try:
        os.remove(db_filename)
    except FileNotFoundError:
        pass

if __name__ == "__main__":
    test()
    import zipme
    zipme.finish(__file__, max_size=2000)

# 10025231703000000000
