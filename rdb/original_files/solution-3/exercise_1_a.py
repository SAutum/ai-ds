def get_query() -> str:
    # BEGIN_SOLUTION

    # Modulo operator works with decimal values
    return "SELECT * FROM product WHERE price % 0.1 = 0"

    # Alternative solution if you prefer integers
    #return "SELECT * FROM product WHERE price * 100 % 10 = 0"

    # END_SOLUTION

    # This is just a placeholder.
    return "SELECT solution FROM brain"
