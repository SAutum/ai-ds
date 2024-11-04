def get_query() -> str:
    # Your solution goes here.
    
    # This is just a placeholder.
    return "SELECT 'Hello,'|| ' ' || firstname || ' ' || lastname AS greeting FROM customer WHERE LOWER(lastname) LIKE '%w%'"
