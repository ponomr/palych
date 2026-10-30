from datetime import timedelta


def business_days(start, end):
    if start > end:
        raise ValueError('start is after end')
    days = 0
    current = start
    while current < end:
        if current.weekday() < 5:
            days += 1
        current += timedelta(days=1)
    return days
