def chunk(items, size):
    """Split items into consecutive pieces of the given size."""
    if size <= 0:
        raise ValueError('size must be positive')
    items = list(items)
    return [items[i:i + size] for i in range(0, len(items), size)]
