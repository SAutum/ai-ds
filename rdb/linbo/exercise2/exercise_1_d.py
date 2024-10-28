def get_query() -> str:
    # Your solution goes here.

    # This query is just a placeholder.
    return "SELECT city.id, city.cityname FROM city JOIN store on city.id = store.city_id JOIN sold_in on store.id = sold_in.store_id JOIN product on sold_in.product_id = product.id WHERE productname = 'Potatoes'"
