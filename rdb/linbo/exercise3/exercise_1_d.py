def get_query() -> str:
    # Your solution goes here.

    # This is just a placeholder.
    return "SELECT customer_id, sum(product.price * purchase.amount) AS total_money_spent FROM product JOIN purchase ON product.product_id = purchase.product_id GROUP BY customer_id ORDER BY total_money_spent DESC LIMIT 1;" 
