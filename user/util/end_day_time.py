from datetime import datetime, timedelta, time


def time_until_end_of_day():
    # type: () -> float
    """
    Get timedelta until end of day on the datetime passed, or current time.
    """
    dt = datetime.now()
    tomorrow = dt + timedelta(days=1)
    return (datetime.combine(tomorrow, time.min) - dt).total_seconds()
