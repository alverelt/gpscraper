from .general import TIMEOUT
from .. import headers
from .. import parsers
from .. import validators

import requests


def details(app_id, lang='en'):
    """Useful info of the app.

    Parameters
    ----------
    app_id : str
        App id/Package name.
    lang : str
        Language to be shown.

    Returns
    -------
    dict | None

    Raises
    ------
    InputTypeError | InputValueError
    """
    validators.details(app_id, lang)
    try:
        response = _do_get_details(app_id, lang)
        return parsers.details(response.text)
    except:
        return None


def _do_get_details(app_id, lang):
    url = 'https://play.google.com/store/apps/details'
    params = {
        'id': app_id, 'hl': lang,
        'gl': 'US', 'showAllReviews': True
    }
    return requests.get(
        url, params=params, headers=headers.GET, timeout=TIMEOUT
    )