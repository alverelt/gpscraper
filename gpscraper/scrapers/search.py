from .. import headers
from .. import parsers
from .. import validators

import logging
import requests


logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s', 
    level=logging.INFO
)


def search(query, lang='us', *args, **kwargs):
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
        while True:
            response = _do_get_search(query, lang)
            
            return parsers.search_first_page(response.text)
    except requests.exceptions.RequestException as e:
        logging.exception(e)
    except Exception as e:
        logging.exception(e)
        logging.error('Unexpected end.')


def _do_get_search(query, lang):
    url = 'https://play.google.com/store/search'
    params = {'q': query, 'hl': lang, 'gl': 'US'}

    return requests.get(url, params=params, headers=headers.GET)