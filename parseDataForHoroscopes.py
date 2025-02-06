"""Because I did not know how to parse the data myself, I found this in the creator
of the Aztro API ' s GitHub profile where he himself had implemented it."""

from dateutil.parser import parse

def parse_date(date_str):
    return parse(date_str).date()

def parse_time(time_str):
    return parse(time_str).time()

def parse_date_range(date_range):
    """returns a tuple of two date objects."""
    dates = date_range.split('-')
    to_return = [parse(dates[0]), parse(dates[1])]
    return to_return