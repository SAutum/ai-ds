def get_query() -> str:
    # Your solution goes here.
    # A question here: why doesn't natural join work here?
    # This is just a placeholder.
    return "SELECT customer_id, SUM(single_money_spent) AS total_money_spent\
             FROM (SELECT purchase.customer_id, product.price * purchase.amount AS single_money_spent\
                FROM purchase JOIN product USING (product_id)) GROUP BY customer_id\
                ORDER BY total_money_spent DESC LIMIT 1"
