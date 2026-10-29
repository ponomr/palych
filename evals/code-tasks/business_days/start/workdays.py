from datetime import timedelta


def business_days(start, end):
    days = 0
    current = start
    while current <= end:
        if current.weekday() < 6:
            days += 1
        current += timedelta(days=1)
    return days
