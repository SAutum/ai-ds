def one_dim_to_n_dim(index: int, grid_size: int, dimension: int) -> tuple[int, ...]:
    """
    Convert a one-dimensional index to an n-dimensional point on a z-curve.

    Parameters
    ----------
    index : int
        A one-dimensional index.
    grid_size : int
        Width and height of the grid. Must be a power of two and at least 2.
    dimension : int
        Dimension of the resulting point.

    Returns
    -------

    point : tuple of ints, len(tuple) = dimension
        The point on the Z-curve corresponding to the index.

    Examples
    --------

        (0, 0) == one_dim_to_n_dim(0, 2, 2)
        (1, 0) == one_dim_to_n_dim(1, 2, 2)
        (0, 1) == one_dim_to_n_dim(2, 2, 2)
        (1, 1) == one_dim_to_n_dim(3, 2, 2)

        (1, 0, 0) == one_dim_to_n_dim(1, 2, 3)
        (0, 1, 0) == one_dim_to_n_dim(2, 2, 3)
        (0, 0, 1) == one_dim_to_n_dim(4, 2, 3)

    """

    # Your solution goes here.
