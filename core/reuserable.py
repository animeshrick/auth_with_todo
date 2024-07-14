from datetime import datetime


def readableDate(requested_date_time):
    return requested_date_time.strftime("%d/%m/%Y %H:%M:%S")


def is_empty_or_none(value):
    """
    Check if a value is empty (e.g., None, empty string, empty list, empty dictionary, etc.).

    Args:
        value: The value to check.

    Returns:
        True if the value is empty or None, False otherwise.

    # Check if a string is empty or None
    result = is_empty_or_none("")  # True
    result = is_empty_or_none("Hello")  # False

    # Check if a list is empty or None
    result = is_empty_or_none([])  # True
    result = is_empty_or_none([1, 2, 3])  # False

    # Check if a dictionary is empty or None
    result = is_empty_or_none({})  # True
    result = is_empty_or_none({"key": "value"})  # False

    # Check if a variable is None
    result = is_empty_or_none(None)  # True

    # Check if an integer is empty or None (not applicable, returns False)
    result = is_empty_or_none(42)  # False
    """
    return value is None or (
        isinstance(value, (str, list, dict, set, tuple)) and not value
    )


nowDateTime = datetime.now()


def nowDateTimeFn():
    return datetime.now().strftime("%d.%m.%Y %H:%M:%S")
