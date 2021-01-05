from bs4 import BeautifulSoup
from .helpers import list_get
from . import headers
from . import forms
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
        validations.lang(value)
        self._lang = value

    def load_headers(self, headers_get=None, headers_post=None):
        if headers_get is not None:
            self.headers_get = headers_get
        if headers_post is not None:
            self.headers_post = headers_post

    def _do_get_app_details(self, id):
        url = 'https://play.google.com/store/apps/details'
        params = {
            'id': id, 'hl': self.lang,
            'gl': 'US', 'showAllReviews': True
        }
        return requests.get(
            url, params=params, headers=self.headers_get,
            timeout=self.TIMEOUT
        )

    def app_details(self, id):
        response = self._do_get_app_details(id)
        return parsers.app_details(response.text)

    def _do_post_next_reviews(self, next_page_form):
        url = 'https://play.google.com/_/PlayStoreUi/data/batchexecute'
        params = {
            'hl': self.lang
        }
        return requests.post(
            url, params=params, headers=self.headers_post, data=next_page_form,
            timeout=self.TIMEOUT
        )

    def reviews(
        self, id, pagination_delay=1, review_size=DEFAULT_REVIEW_SIZE,
        sort_type=forms.Sort.MOST_RELEVANT, sort_score=None
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
        sort_score : int | None
            Sort by number of score.

        Yields
        ------
        list of dict
        """
        validations.id(id)
        validations.review_size(review_size)
        validations.sort_type(sort_type)

        page = 1
        try:
            print(f'Page {page}')
            response = self._do_get_app_details(id)
            reviews, token = parsers.reviews_first_page(response.text)

            # If either sort_type or sort_score has value, we must skip this
            # because by default, Google shows "Most relevant" and
            # "All ratings" reviews.
            if not sort_type and not sort_score:
                yield reviews

            form_next_page = forms.reviews_next_page(
                id, token, review_size, sort_type, sort_score
            )

            if form_next_page:
                finished = False

                while not finished:
                    page += 1
                    time.sleep(pagination_delay)
                    print(f'Page {page}', end='')
                    response = self._do_post_next_reviews(
                        form_next_page
                    )
                    reviews, token = parsers.reviews_next_page(
                        response.text
                    )
                    form_next_page = forms.reviews_next_page(
                        id, token, review_size, sort_type, sort_score
                    )

                    yield reviews

                    finished = not bool(form_next_page)
        except:
            print(traceback.format_exc(chain=False))
            print('Unexpected end.')
            pass
        finally:
            print('End of scrape, if your list is empty, please try again.')
