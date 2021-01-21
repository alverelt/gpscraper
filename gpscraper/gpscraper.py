from bs4 import BeautifulSoup
from .utils import list_get
from . import headers
from . import forms
from . import parsers
from . import validations

import requests
import time


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
        """Useful info of the app.

        Parameters
        ----------
        id : str
            App id/Package name.

        Returns
        -------
        dict | None
        """ 
        try:
            response = self._do_get_app_details(id)
            return parsers.app_details(response.text)
        except:
            return None

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
        self, id, 
        count_pages=0, 
        pagination_delay=1, 
        review_size=DEFAULT_REVIEW_SIZE, 
        sort_type=forms.Sort.MOST_RELEVANT, 
        sort_score=None):
        """Generator, gets all reviews.

        Parameters
        ----------
        id : str
            App id/Package name.
        count_pages : int
            Number of pages to scrape, if count_pages == 0, scrapes all pages.
        pagination_delay : int | float
            Time between each scrape.
        review_size : int
            Reviews by page, except page 1.
        sort_type : str
            Sorting type. Check Sort class.
        sort_score : int | None
            Sort by number of score.

        Notes
        -----
            If either review_size, sort_type or sort_score are invalid,
        default values will be used.

        +-------------+-------------------+
        | VARIABLE    | DEFAULTS TO       |       
        +-------------+-------------------+
        | review_size | 40                |
        | sort_type   | MOST_RELEVANT     |
        | sort_score  | None (ALL SCORES) |
        +-------------+-------------------+
        
        Yields
        ------
        list of dict

        Raises
        ------
        (TypeError | ValueError) when invalid id.
        
        """
        validations.id(id)

        if not isinstance(count_pages, int) or count_pages < 0:
            count_pages = 0

        if (not isinstance(pagination_delay, (int, float)) 
                or pagination_delay < 0):
            pagination_delay = 1

        page = 1
        try:
            if not sort_type and not sort_score:
                response = self._do_get_app_details(id)
                reviews, token = parsers.reviews_first_page(response.text)
            else:
                form_next_page = forms.reviews_next_page(
                    id, None, review_size, sort_type, sort_score
                )
                response = self._do_post_next_reviews(form_next_page)
                reviews, token = parsers.reviews_next_page(response.text)

            yield reviews

            while token and (count_pages == 0 or page < count_pages):
                form_next_page = forms.reviews_next_page(
                    id, token, review_size, sort_type, sort_score
                )
                page += 1
                time.sleep(pagination_delay)
                response = self._do_post_next_reviews(form_next_page)
                reviews, token = parsers.reviews_next_page(response.text)
                yield reviews

        except Exception as e:
            print(e)
            print('Unexpected end.')
        finally:
            print('End of scrape.')
