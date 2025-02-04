def n_dim_to_one_dim(point: tuple[int, ...], grid_size: int, dimension: int) -> int:
    """
    Convert an n-dimensional point on a Z-curve to a one-dimensional index.

    Parameters
    ----------
    point : tuple of ints, len(tuple) = dimension
        The point on the Z-curve.
    grid_size : int
        Width and height of the grid. Must be a power of two and at least 2.
    dimension : int
        Dimension of the resulting point.

    Returns
    -------
    index : int
        A one-dimensional index corresponding to the point.

    """

    # Your solution goes here.
