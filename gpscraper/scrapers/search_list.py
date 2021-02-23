from .. import headers
from .. import parsers
from .. import validators

import logging
import requests


logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s', 
    level=logging.INFO
)


def search_list(query, lang='us', *args, **kwargs):
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
    # validators.search_list(query, lang)

    try:
        while True:
            response = _do_get_search_list(query, lang)
            
            return parsers.search_list_first_page(response.text)
    except requests.exceptions.RequestException as e:
        logging.exception(e)
    except Exception as e:
        logging.exception(e)
        logging.error('Unexpected end.')


def _do_get_search_list(query, lang):
    url = 'https://play.google.com/store/search'
    params = {'q': query, 'hl': lang, 'gl': 'US'}

    return requests.get(url, params=params, headers=headers.GET)