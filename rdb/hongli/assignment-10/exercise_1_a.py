def create_index() -> str:

    return """

    CREATE INDEX index_pixel_rgbxy ON pixel (r, g, b, x, y)

    """
