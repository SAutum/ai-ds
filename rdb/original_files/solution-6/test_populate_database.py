import os
import csv
import time
import random
import psycopg


def load_csv(path: str):
    with open(path, encoding="utf-8") as f:
        reader = csv.reader(f)
        headers = next(reader)
        rows = list(reader)
        columns = dict(zip(headers, zip(*rows)))
        return columns


def weighted_sample(columns, id_column, size) -> list[int]:
    weights = [float(w) for w in columns["weight"]]
    return random.choices(columns[id_column], weights, k=size)


def create_sales_csv() -> None:
    print("creating temporary sale.csv...")
    product = load_csv("product.csv")
    timestamp = load_csv("timestamp.csv")
    shop = load_csv("shop.csv")

    random.seed(0)

    # newline="" is required for Windows to write "\r\n" instead of "\r\r\n"
    with open("sale.csv", "w", encoding="utf-8", newline="") as f:
        headers = ["sale_id", "shop_id", "product_id", "timestamp_id", "quantity"]
        writer = csv.writer(f)
        writer.writerow(headers)
        # Create data in batches to reduce memory usage
        size = 1000
        for sale_id in range(0, 1000_000, size):
            sale_ids = list(range(sale_id, sale_id + size))
            shop_ids = weighted_sample(shop, "shop_id", size)
            product_ids = weighted_sample(product, "product_id", size)
            timestamp_ids = weighted_sample(timestamp, "timestamp_id", size)
            quantities = [random.randint(1, 10) for _ in range(size)]

            for row in zip(sale_ids, shop_ids, product_ids, timestamp_ids, quantities):
                writer.writerow(row)


def populate_database() -> None:
    start_time = time.perf_counter()

    with psycopg.connect() as conn:
        create_sales_csv()

        print("populating database...")

        with conn.cursor() as cursor:
            # Delete sale, product, shop and timestamp tables if they exist
            cursor.execute("DROP TABLE IF EXISTS sale CASCADE")
            cursor.execute("DROP TABLE IF EXISTS product CASCADE")
            cursor.execute("DROP TABLE IF EXISTS shop CASCADE")
            cursor.execute("DROP TABLE IF EXISTS timestamp CASCADE")

            # Create tables
            cursor.execute(
                """
            CREATE TABLE timestamp (
                timestamp_id BIGSERIAL PRIMARY KEY,
                year INTEGER,
                month TEXT,
                day INTEGER,
                hour INTEGER,
                minute INTEGER,
                second INTEGER,
                quarter INTEGER,
                weekday TEXT,
                isotime TEXT,
                weight INTEGER
            )
            """
            )

            cursor.execute(
                """
            CREATE TABLE shop (
                shop_id BIGSERIAL PRIMARY KEY,
                branch TEXT,
                state TEXT,
                city TEXT,
                city_population INTEGER,
                city_area REAL,
                city_geolocation TEXT,
                weight INTEGER
            )
            """
            )

            cursor.execute(
                """
            CREATE TABLE product (
                product_id BIGSERIAL PRIMARY KEY,
                name TEXT,
                rating REAL,
                price NUMERIC(20, 2),
                reviews INTEGER,
                category TEXT,
                subcategory TEXT,
                weight INTEGER
            )
            """
            )

            cursor.execute(
                """
            CREATE TABLE sale (
                sale_id BIGSERIAL PRIMARY KEY,
                shop_id INTEGER REFERENCES shop(shop_id),
                product_id INTEGER REFERENCES product(product_id),
                timestamp_id INTEGER REFERENCES timestamp(timestamp_id),
                quantity INTEGER
            )
            """
            )

            # Copy data from CSV files into database
            for table in ["timestamp", "shop", "product", "sale"]:
                with open(f"{table}.csv", encoding="utf-8") as f:
                    text = f.read()

                with cursor.copy(f"COPY {table} FROM STDIN WITH CSV HEADER") as copy:
                    copy.write(text)

            # Remove columns previously used for generating sales
            cursor.execute("ALTER TABLE timestamp DROP COLUMN weight")
            cursor.execute("ALTER TABLE shop DROP COLUMN weight")
            cursor.execute("ALTER TABLE product DROP COLUMN weight")

    os.remove("sale.csv")
    elapsed_time = time.perf_counter() - start_time
    print(f"done in {elapsed_time:.3f} seconds")


if __name__ == "__main__":
    populate_database()

# 65371040162000000000
