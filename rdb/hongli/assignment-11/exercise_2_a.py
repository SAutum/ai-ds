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

    # check if index is within bounds
    if index < 0 or index >= grid_size ** dimension:
        raise ValueError("Index out of bounds.")

    # convert index to n-dimensional indices
    n_dim_indices = []
    for d in range(dimension):
        _bindex = index >> d
        n_dim_index = ''
        # using string and binary operations to get the n-dimensional index
        for i in range(grid_size):
            n_dim_index = bin(_bindex)[-1] + n_dim_index
            _bindex = _bindex >> dimension
        n_dim_indices.append(int(n_dim_index, 2))

    return tuple(n_dim_indices)
