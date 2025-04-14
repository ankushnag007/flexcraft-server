from datetime import datetime, timezone

import pytz

# Constants for country -> timezone mapping
COUNTRY_TIMEZONES = {
    "US": "America/New_York",
    "IN": "Asia/Kolkata",
    "UK": "Europe/London",
    "AU": "Australia/Sydney",
    "CA": "America/Toronto",
    "DE": "Europe/Berlin",
    # Add more as needed
}


def get_current_utc_datetime():
    """Returns current UTC datetime"""
    return datetime.now(timezone.utc)


def convert_utc_to_country_time(utc_datetime: datetime, country_code: str) -> datetime:
    """
    Converts UTC datetime to the given country's local time.
    Args:
        utc_datetime (datetime): A timezone-aware UTC datetime.
        country_code (str): Country code as per COUNTRY_TIMEZONES (e.g., 'IN', 'US')
    Returns:
        datetime: Converted datetime in the target country's timezone.
    """
    if not utc_datetime.tzinfo:
        # ensure it's UTC-aware if passed as naive
        utc_datetime = utc_datetime.replace(tzinfo=pytz.utc)

    timezone_str = COUNTRY_TIMEZONES.get(country_code.upper())
    if not timezone_str:
        raise ValueError(f"Unsupported country code: {country_code}")

    target_timezone = pytz.timezone(timezone_str)
    return utc_datetime.astimezone(target_timezone)
