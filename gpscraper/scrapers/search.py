from .. import forms
from .. import headers
from .. import parsers
from .. import validators

import logging
import requests


logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s', 
    level=logging.INFO
)


def search(
    query, 
    token=None, 
    pagination_delay=1, 
    lang='us', 
    *args, **kwargs):
    """List every content according on the query.

    Parameters
    ----------
    query : str
        Search query.
    lang : str
        Language of results.
    
    Yields
    ------
    list of dict

    Raises
    ------
    InputTypeError | InputValueError
    
    """
    validators.search(query, lang)

    try:
        token = token or -1
        while token:
            if token == -1:
                response = _do_get_search(query, lang)
                results, token, strange_data =  parsers.search_first_page(
                    response.text
                )
            else:
                form_next_page = forms.search_next_page(token, strange_data)

            return {
                'search': results,
                'token': token,
                'strange_data': strange_data
            }

    except requests.exceptions.RequestException as e:
        logging.exception(e)
    except Exception as e:
        logging.exception(e)
        logging.error('Unexpected end.')


def _do_get_search(query, lang):
    url = 'https://play.google.com/store/search'
    params = {'q': query, 'hl': lang, 'gl': 'US'}

    return requests.get(url, params=params, headers=headers.GET)
