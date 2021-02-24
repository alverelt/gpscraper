from .exceptions import InputTypeError, InputValueError
from .forms import SortType


def details(app_id, lang):
    if not isinstance(app_id, str):
        raise TypeError("'app_id' must be of type str.")
    if not id:
        raise ValueError("'app_id' cannot be empty.")

    if not isinstance(lang, str):
        raise TypeError("'lang' must be of type str.")
    if not lang:
        raise ValueError("'lang' cannot be empty.")


def reviews(
        app_id, token, pagination_delay, review_size, 
        sort_type, rating, lang):
    if not isinstance(app_id, str):
        raise TypeError("'app_id' must be of type str.")
    if not app_id:
        raise ValueError("'app_id' cannot be empty.")

    if not isinstance(token, str) and token is not None:
        raise TypeError("'token' must be either type str or None.")
    if isinstance(token, str) and not token:
        raise ValueError("'token' cannot be empty.")

    if not isinstance(pagination_delay, (int, float)):
        raise TypeError("'pagination_delay' must be of type (int | float).")
    if pagination_delay < 0:
        raise ValueError("'pagination_delay' can not be negative.")

    if not isinstance(review_size, int):
        raise TypeError("'review_size' must be of type int.")
    if review_size < 1:
        raise ValueError("'review_size' must be greater than 0.")

    if sort_type not in SortType:
        raise ValueError("'sort_type' value is not recognized.")

    if not isinstance(rating, int):
        raise TypeError("'rating' must be of type int.")
    if not (0 <= rating <= 5):
        raise ValueError("'rating' must be between 0 and 5.")

    if not isinstance(lang, str):
        raise TypeError("'lang' must be of type str.")
    if not lang:
        raise ValueError("'lang' cannot be empty.")


def review_history(app_id, review_id):
    if not isinstance(app_id, str):
        raise TypeError("'app_id' must be of type str.")
    if not app_id:
        raise ValueError("'app_id' cannot be empty.")

    if not isinstance(review_id, str):
        raise TypeError("'review_id' must be of type str.")
    if not review_id:
        raise ValueError("'review_id' cannot be empty.")


def search(query, lang):
    if not isinstance(query, str):
        raise TypeError('query must be of type str.')
    if not query:
        raise ValueError('query cannot be empty.')

    if not isinstance(lang, str):
        raise TypeError("'lang' must be of type str.")
    if not lang:
        raise ValueError("'lang' cannot be empty.")