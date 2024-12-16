def get_values() -> list[int]:
    # BEGIN_SOLUTION

    return [1, 1]

    # Explanation

    """
    The RANK() function will assign the same rank to rows with the same values,
    while the ROW_NUMBER() function will assign a unique integer to each row based
    on the ordering specified in the OVER clause.
    """

    # END_SOLUTION
