def get_query() -> str:
    # Your solution goes here.

    # This query is just a placeholder.
    return "SELECT customer.id, customer.firstname, customer.lastname FROM customer JOIN purchase ON purchase.customer_id = customer.id GROUP BY customer.id, customer.firstname, customer.lastname HAVING COUNT(purchase.id)=5 AND SUM(purchase.amount) >= 28"
