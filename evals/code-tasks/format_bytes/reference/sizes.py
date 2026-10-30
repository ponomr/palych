UNITS = ['KB', 'MB', 'GB', 'TB']


def format_bytes(n):
    if n < 0:
        raise ValueError('negative size')
    if n < 1024:
        return f'{n} B'
    value, unit = n / 1024, 0
    while unit < len(UNITS) - 1 and round(value, 1) >= 1024:
        value /= 1024
        unit += 1
    return f'{round(value, 1):.1f}'.removesuffix('.0') + ' ' + UNITS[unit]
