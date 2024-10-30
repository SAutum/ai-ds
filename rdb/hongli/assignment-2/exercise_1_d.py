def get_query() -> str:
    # Your solution goes here.

    # This query is just a placeholder.
    return "SELECT * FROM city WHERE id IN \
        ( SELECT city_id FROM store WHERE id IN \
            (SELECT store_id FROM sold_in WHERE product_id IN \
                (SELECT id FROM product WHERE productname ='Potatoes') \
            ) \
        )"
