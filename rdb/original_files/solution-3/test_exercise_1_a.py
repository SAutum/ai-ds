from exercise_1_a import get_query
from typing import List, Any
from decimal import Decimal
import psycopg
import random
import zipme


def test_sql_query(
    query: str,
    expected_attribute_names: List[str],
    expected_result: Any,
    compare_sets: bool = True,
    expected: List[Any] = [],
) -> None:
    assert '"' not in query, "SQL strings must be single-quoted"

    query = query.rstrip("; \t\r\n")

    assert query.count(";") == 0, "A semicolon is not necessary. Only one query is allowed."

    cursor = initialize_database()

    cursor.execute(query)

    if expected:
        for expectation in expected:
            cursor.execute(expectation["query"])

            result = list(cursor)

            assert result == expectation["result"], f"Expected {expectation['result']}\nbut got {result}."

    else:
        attribute_names = [description.name for description in cursor.description]

        names_are_equal = True

        if len(attribute_names) != len(expected_attribute_names):
            names_are_equal = False
        else:
            for name1, name2 in zip(attribute_names, expected_attribute_names):
                if name1 != name2 and name2 != "any name":
                    names_are_equal = False

        assert names_are_equal, (
            f"Expected attributes: {', '.join(expected_attribute_names)}\n"
            f"but got attributes: {', '.join(attribute_names)}."
        )

        result = list(cursor)

        if compare_sets:
            assert set(result) == set(expected_result), f"Expected {expected_result}\nbut got {result}."
        else:
            assert result == expected_result, f"Expected {expected_result}\nbut got {result}."


def initialize_database() -> Any:
    random.seed(0)

    connection = psycopg.connect()

    cursor = connection.cursor()

    cursor.execute("DROP TABLE IF EXISTS purchase CASCADE")
    cursor.execute("DROP TABLE IF EXISTS product CASCADE")
    cursor.execute("DROP TABLE IF EXISTS customer CASCADE")
    cursor.execute("DROP TABLE IF EXISTS store CASCADE")

    cursor.execute("""
    CREATE TABLE product (
        product_id INTEGER PRIMARY KEY,
        price NUMERIC(6, 2),
        productname TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE store (
        store_id INTEGER PRIMARY KEY
    )
    """)

    cursor.execute("""
    CREATE TABLE customer (
        customer_id INTEGER PRIMARY KEY,
        firstname TEXT,
        lastname TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE purchase (
        purchase_id INTEGER PRIMARY KEY,
        customer_id INTEGER REFERENCES customer (customer_id),
        store_id    INTEGER REFERENCES store    (store_id),
        product_id  INTEGER REFERENCES product  (product_id),
        amount INTEGER
    )
    """)

    # Create products
    products = [
        (0, 3.50, "Fish"),
        (1, 150.72, "Apple"),
        (2, 0.60, "Banana"),
        (3, 6.00, "Pizza"),
        (4, 19.99, "Duck"),
        (5, 9999.99, "Printer Ink"),
    ]

    query = """
    INSERT INTO product (
        product_id,
        price,
        productname
    ) VALUES (%s, %s, %s)
    """

    cursor.executemany(query, products)

    # Create stores
    stores = [[i] for i in range(10)]
    cursor.executemany("INSERT INTO store (store_id) VALUES (%s)", stores)

    # Generate random customers
    firstnames = [
        "John",
        "Jane",
        "Bob",
        "Alice",
        "Peter",
        "Paul",
        "Mary",
        "Sue",
        "Bill",
        "Joe",
    ]

    lastnames = [
        "Smith",
        "Jones",
        "Brown",
        "Taylor",
        "Williams",
        "Wilson",
        "Johnson",
        "White",
        "Roberts",
        "Thompson",
    ]

    customers = [(customer_id, random.choice(firstnames), random.choice(lastnames)) for customer_id in range(20)]

    query = """
    INSERT INTO customer (
        customer_id,
        firstname,
        lastname
    ) VALUES (%s, %s, %s)
    """

    cursor.executemany(query, customers)

    # Create a customer with a random firstname
    firstname = random.choice(firstnames)

    query = """
    INSERT INTO customer (
        customer_id,
        firstname,
        lastname
    ) VALUES (%s, %s, %s)
    """

    cursor.execute(query, (20, firstname, None))

    # Create a customer named Test Customer
    query = """
    INSERT INTO customer (
        customer_id,
        firstname,
        lastname
    ) VALUES (%s, %s, %s)
    """

    cursor.execute(query, (21, "Test", "Customer"))

    # Create purchases
    for purchase_id in range(20):
        customer_id = random.choice(customers)[0]
        store_id = random.choice(stores)[0]
        product_id = random.choice(products)[0]
        amount = random.randrange(1, 10)

        # Numbers work out nicer this way
        if customer_id == 5:
            amount += 1

        query = """
        INSERT INTO purchase (
            purchase_id,
            customer_id,
            store_id,
            product_id,
            amount
        ) VALUES (
            %(purchase_id)s,
            %(customer_id)s,
            %(store_id)s,
            %(product_id)s,
            %(amount)s
        )
        """

        data = {
            "purchase_id": purchase_id,
            "customer_id": customer_id,
            "store_id": store_id,
            "product_id": product_id,
            "amount": amount,
        }

        cursor.execute(query, data)

    connection.commit()

    return cursor


if __name__ == "__main__":
    expected = [
        (0, Decimal("3.50"), "Fish"),
        (2, Decimal("0.60"), "Banana"),
        (3, Decimal("6.00"), "Pizza"),
    ]

    expected_attributes = ["product_id", "price", "productname"]

    test_sql_query(get_query(), expected_attributes, expected)
    zipme.finish(__file__)

# 63447406362000000000
