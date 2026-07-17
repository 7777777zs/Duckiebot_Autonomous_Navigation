"""Freshness checks shared by motion nodes."""


def is_detection_fresh(timestamp, now, timeout):
    """Return false for missing, future, or expired timestamps."""
    if timestamp is None or timeout < 0:
        return False
    age = now - timestamp
    return 0.0 <= age <= timeout
