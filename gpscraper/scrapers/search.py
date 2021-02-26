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
    unknown_list_1=None,
    pagination_delay=1, 
    lang='us'):
    """List every content according on the query.

    Parameters
    ----------
    query : str
        Search query.
    token : str
        For continuation of search, you must provide this token.
    unknown_list_1 : str
        For continuation of search, you must provide this unknown_list_1.
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
                results, token, unknown_list_1 =  parsers.search_first_page(
                    response.text
                )
            else:
                form_next_page = forms.search_next_page(token, unknown_list_1)
                response = _do_post_next_search(form_next_page, lang)
                results, token = parsers.search_next_page(
                    response.text
                )

            yield {
                'search': results,
                'continue': {
                    'token': token,
                    'unknown_list_1': unknown_list_1
                }
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


def _do_post_next_search(form_next_page, lang):
    url = 'https://play.google.com/_/PlayStoreUi/data/batchexecute'
    params = {'hl': lang, 'gl': 'US'}

    return requests.post(
        url, params=params, headers=headers.POST, data=form_next_page
    )
