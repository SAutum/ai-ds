def get_query() -> str:
    # Your solution goes here.

    # This query is just a placeholder.
    return "SELECT * FROM customer WHERE id NOT IN \
    (SELECT DISTINCT customer_id FROM purchase WHERE product_id IN \
        (SELECT id FROM product WHERE productname='Pizza'))\
            ORDER BY lastname DESC"
