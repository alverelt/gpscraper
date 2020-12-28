from bs4 import BeautifulSoup
from .helpers import list_get
from . import headers
from . import parsers
from . import validations

import json
import requests
import time
import traceback


class GPScraper:
    TIMEOUT = 30
    DEFAULT_REVIEW_SIZE = 40

    def __init__(self, lang='', *args, **kwargs):
        self.lang = lang
        self.load_headers(headers.GET, headers.POST)

    @property
    def lang(self):
        return self._lang

    @lang.setter
    def lang(self, value):
        if value != getattr(self, '_lang', ''):
            self.cache_app_details = None

        validations.lang(value)
        self._lang = value
    
    def load_headers(self, headers_get=None, headers_post=None):
        if headers_get is not None:
            self.headers_get = headers_get
        if headers_post is not None:
            self.headers_post = headers_post

    def _do_get_app_details(self, id, *args, **kwargs):
        url = 'https://play.google.com/store/apps/details'
        params = {
            'id': id, 'hl': self.lang,
            'gl': 'US', 'showAllReviews': True
        }        
        return requests.get(
            url, params=params, headers=self.headers_get, 
            timeout=self.TIMEOUT, *args, **kwargs
        )

    def app_details(self, id, *args, **kwargs):
        response = self._do_get_app_details(id, *args, **kwargs)
        return parsers.parse_app_details(response.text)

    def _do_post_next_reviews(self, next_page_form, *args, **kwargs):
        url = 'https://play.google.com/_/PlayStoreUi/data/batchexecute'
        params = {
            'hl': self.lang
        }
        return requests.post(
            url, params=params, headers=self.headers_post, data=next_page_form,
            timeout=self.TIMEOUT, *args, **kwargs
        )

    def reviews(
        self, id, pagination_delay=1, review_size=DEFAULT_REVIEW_SIZE, 
        sort_type=None, *args, **kwargs
    ):
        """Generator, gets all reviews.

        Parameters
        ----------
        id : str
            Url parameter (Application identification).
        pagination_delay : int | float
            Time between each scrape.
        review_size : int
            Reviews by page, except page 1.
        sort_type : str
            Sorting type.
        **kwargs:
            Optional params for requests.

        Yields
        ------
        list of dict
        """
        validations.id(id)
        validations.review_size(review_size)
        validations.sort_type(sort_type)

        # Headers will be removed, because it must be passed through
        # headers_get or headers_post to differentiate both.
        kwargs.pop('headers', None)

        page = 1
        try:
            print(f'Page {page}', end='')
            response = self._do_get_app_details(id, *args, **kwargs)
            reviews, token = parsers.parse_first_page(response.text)

            next_page_form = self._prepare_form_next_page(
                id, token, review_size, sort_type
            )
            print(f', Gathered {len(reviews)}')

            yield reviews

            if next_page_form:
                finished = False
                while not finished:
                    page += 1
                    time.sleep(pagination_delay)
                    print(f'Page {page}', end='')
                    response = self._do_post_next_reviews(
                        next_page_form, *args, **kwargs
                    )
                    reviews, token = parsers.parse_next_page(
                        response.text
                    )
                    next_page_form = self._prepare_form_next_page(
                        id, token, review_size, sort_type
                    )
                    print(f', Gathered {len(reviews)}')

                    yield reviews

                    finished = not bool(next_page_form)
        except:
            print(traceback.format_exc(chain=False))
            print('Unexpected end.')
            pass
        finally:
            print('End of scrape, if your list is empty, please try again.')

    def _prepare_form_next_page(self, id, next_page_token, review_size, sort_type):
        if not next_page_token:
            return None

        # This should remain None, its implementation is not done yet.
        sort_type = None
        sort_type = json.dumps(sort_type)

        long_data = (
            f'[null,null,[2,{sort_type},[{review_size},null,'
            f'"{next_page_token}"],null,[]],["{id}",7]]'
        )
        form = {
            'f.req': [[[
                'UsvDTd',
                long_data,
                None,
                'generic'
            ]]]
        }

        form['f.req'] = json.dumps(form['f.req'], separators=(',', ':'))
        return form
