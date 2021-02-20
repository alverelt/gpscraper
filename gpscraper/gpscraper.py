from bs4 import BeautifulSoup
from .utils import list_get
from . import headers
from . import forms
from . import parsers
from . import validators

import logging
import requests
import requests.exceptions
import time


logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s', 
    level=logging.INFO
)


class GPScraper:
    TIMEOUT = 30

    def __init__(self, lang='', *args, **kwargs):
        self.lang = lang
        self.load_headers(headers.GET, headers.POST)

    @property
    def lang(self):
        return self._lang

    @lang.setter
    def lang(self, value):
        validators.lang(value)
        self._lang = value

    def load_headers(self, headers_get=None, headers_post=None):
        if headers_get is not None:
            self.headers_get = headers_get
        if headers_post is not None:
            self.headers_post = headers_post

    def _do_get_app_details(self, app_id):
        url = 'https://play.google.com/store/apps/details'
        params = {
            'id': app_id, 'hl': self.lang,
            'gl': 'US', 'showAllReviews': True
        }
        return requests.get(
            url, params=params, headers=self.headers_get,
            timeout=self.TIMEOUT
        )

    def app_details(self, app_id):
        """Useful info of the app.

        Parameters
        ----------
        app_id : str
            App id/Package name.

        Returns
        -------
        dict | None

        Raises
        ------
        InputTypeError | InputValueError
        """
        validators.app_details(app_id)
        try:
            response = self._do_get_app_details(app_id)
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
        self, app_id, count_pages=0, pagination_delay=1, review_size=100, 
        sort_type=forms.SortType.MOST_RELEVANT, score=0):
        """Generator, gets all reviews.

        Parameters
        ----------
        app_id : str
            App id/Package name.
        count_pages : int
            Number of pages to scrape, if count_pages == 0, scrapes all pages.
        pagination_delay : int | float
            Time between each scrape.
        review_size : int
            Reviews by page, except page 1.
        sort_type : str
            Sorting type. Check Sort class.
        score : int
            Shows reviews by score. Zero (0) means all scores. 
        
        Yields
        ------
        list of dict

        Raises
        ------
        InputTypeError | InputValueError
        
        """
        validators.reviews(
            app_id, count_pages, pagination_delay, review_size,
            sort_type, score
        )
       
        try:
            page = 1
            token = 1
            while token and (count_pages == 0 or page <= count_pages):
                # The only time we do a GET request to first page is
                # when sort_type and score are default values.
                if page == 1 and not sort_type and not score:
                    response = self._do_get_app_details(app_id)
                    reviews, token = parsers.reviews_first_page(response.text)
                else:
                    form_next_page = forms.reviews_next_page(
                        app_id, None if page == 1 else token, 
                        review_size, sort_type, score
                    )
                    response = self._do_post_next_reviews(form_next_page)
                    reviews, token = parsers.reviews_next_page(response.text)
                
                yield {
                    'reviews': reviews,
                    'continue': {
                        'app_id': app_id,
                        'lang': self.lang,
                        'review_size': review_size,
                        'sort_type': sort_type,
                        'score': score,
                        'token': token
                    }
                }
                
                page += 1
                time.sleep(pagination_delay)
        except GeneratorExit:
            return
        except requests.exceptions.RequestException as e:
            logging.exception(e)
        except Exception as e:
            logging.exception(e)
            logging.error('Unexpected end.')

    def _do_get_review_history(self, form):
        url = 'https://play.google.com/_/PlayStoreUi/data/batchexecute'

        return requests.post(
            url, headers=self.headers_post, data=form,
            timeout=self.TIMEOUT
        )

    def review_history(self, app_id, review_id):
        """Gets a review history (all modifications).

        Parameters
        ----------
        app_id : str
            App id/Package name.
        review_id : int
            Review id, it is retrieve from reviews when you use the
            reviews method.
        
        Yields
        ------
        list of dict | None

        Raises
        ------
        InputTypeError | InputValueError        
        """
        validators.review_history(app_id, review_id)
        try:
            form = forms.review_history(app_id, review_id)
            response = self._do_get_review_history(form)
            return parsers.review_history(response.text)
        except:
            return None