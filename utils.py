from datetime import datetime
import os


def time_check(days, datetime_variable):
    """
    Checks .env variable for the time to see if its within set days returns True if within the days and False if it needs to be refreshed
    """
    last_refresh = os.getenv(datetime_variable)
    last_refresh = datetime.strptime(last_refresh, '%Y-%m-%d %H:%M:%S.%f')
    now = datetime.now()
    diff = now - last_refresh
    # checks if the difference calculated is 24 hours or greater
    if diff.days <= days - 1:
        # if inside of target time return True
        return True
    # Otherwise return False
    return False
