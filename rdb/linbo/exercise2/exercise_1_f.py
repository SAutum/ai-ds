def get_query() -> str:
    # Your solution goes here.

    # This query is just a placeholder.
    return "SELECT customer.id, customer.firstname, customer.lastname FROM customer JOIN purchase ON purchase.customer_id = customer.id JOIN product ON product.id = purchase.product_id WHERE customer.id NOT IN(SELECT customer.id FROM customer JOIN purchase ON purchase.customer_id = customer.id JOIN product ON product.id = purchase.product_id WHERE product.productname = 'Pizza') GROUP BY customer.id, customer.firstname, customer.lastname ORDER BY customer.lastname DESC"
