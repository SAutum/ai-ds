def get_query() -> str:
    # BEGIN_SOLUTION

    return """
    SELECT
        city.id, city.cityname
    FROM
        sold_in
        JOIN store ON
            sold_in.store_id = store.id
        JOIN product ON
            sold_in.product_id = product.id
        JOIN city ON
            store.city_id = city.id
    WHERE
        productname = 'Potatoes'
    ORDER BY
        city.id
    """

    # END_SOLUTION

    # This query is just a placeholder.
    return "SELECT attribute FROM relation"
