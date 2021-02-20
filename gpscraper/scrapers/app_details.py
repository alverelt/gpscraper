from .. import headers
from .. import parsers
from .. import validators

import requests


def app_details(app_id, lang='us'):
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
    validators.app_details(app_id, lang)
    try:
        response = _do_get_app_details(app_id, lang)
        return parsers.app_details(response.text)
    except:
        return None


def _do_get_app_details(app_id, lang, *args, **kwargs):
    url = 'https://play.google.com/store/apps/details'
    params = {
        'id': app_id, 'hl': lang,
        'gl': 'US', 'showAllReviews': True
    }

    return requests.get(
        url, params=params, headers=headers.GET
    )