def chunk(items, size):
    """Split items into consecutive pieces of the given size."""
    return [items[i:i + size] for i in range(0, len(items) - size + 1, size)]
