"""
Notes
-----
- InputTypeError and InputValueError are used when validating arguments
in parsing functions so we can use TypeError and ValueError to catch other
types of errors.
"""
from .exceptions import InputTypeError, InputValueError
from .forms import Sort


def lang(value):
    if not isinstance(value, str):
        raise TypeError('Lang must be of type str.')
    if not value:
        raise ValueError('Lang cannot be empty.')


def app_details(id):
    if not isinstance(id, str):
        raise InputTypeError("'id' must be of type str.")
    if not id:
        raise InputValueError("'id' cannot be empty.")


def reviews(
        id, count_pages, pagination_delay,
        review_size, sort_type, score):
    if not isinstance(id, str):
        raise InputTypeError("'id' must be of type str.")
    if not id:
        raise InputValueError("'id' cannot be empty.")

    if not isinstance(count_pages, int):
        raise InputTypeError("'count_pages' must be of type int.")
    if count_pages < 0:
        raise InputValueError("'count_pages' can not be negative.")

    if not isinstance(pagination_delay, (int, float)):
        raise InputTypeError("'pagination_delay' must be of type (int | float).")
    if count_pages < 0:
        raise InputValueError("'pagination_delay' can not be negative.")

    if not isinstance(review_size, int):
        raise InputTypeError("'review_size' must be of type int.")
    if review_size < 1:
        raise InputValueError("'review_size' must be greater than 0.")

    if not Sort.contains(sort_type):
        raise InputValueError("'sort_type' value is not recognized.")

    if not isinstance(score, int):
        raise InputTypeError("'score' must be of type int.")
    if not (0 <= score <= 5):
        raise InputValueError("'score' must be between 0 and 5.")




