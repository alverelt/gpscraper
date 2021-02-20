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

    @classmethod
    def _do_get_app_details(cls, app_id, lang, *args, **kwargs):
        url = 'https://play.google.com/store/apps/details'
        params = {
            'id': app_id, 'hl': lang,
            'gl': 'US', 'showAllReviews': True
        }
        return requests.get(
            url, params=params, headers=headers.GET,
            timeout=cls.TIMEOUT
        )

    @classmethod
    def app_details(cls, app_id, lang='us'):
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
            response = cls._do_get_app_details(app_id, lang)
            return parsers.app_details(response.text)
        except:
            return None

    @classmethod
    def _do_post_next_reviews(cls, next_page_form, lang, *args, **kwargs):
        url = 'https://play.google.com/_/PlayStoreUi/data/batchexecute'
        params = {
            'hl': lang
        }
        return requests.post(
            url, params=params, headers=headers.POST, data=next_page_form,
            timeout=cls.TIMEOUT
        )

    @classmethod
    def reviews(
        cls, app_id, token=None, pagination_delay=1, review_size=100, 
        sort_type=forms.SortType.MOST_RELEVANT, score=0, lang='us',
        *args, **kwargs):
        """Generator, gets all reviews.

        Parameters
        ----------
        app_id : str
            App id/Package name.
        token : str | None
            For continuation of reviews, you must provide this token.
        pagination_delay : int | float
            Time between each scrape.
        review_size : int
            Reviews by page, except page 1.
        sort_type : SortType
            Sorting type. Check SortType class.
        score : int
            Shows reviews by score. Zero (0) means all scores. 
        lang : str
            Language of reviews.
        
        Yields
        ------
        list of dict

        Raises
        ------
        InputTypeError | InputValueError
        
        """
        validators.reviews(
            app_id, token, pagination_delay, review_size, sort_type, 
            score, lang
        )
       
        try:
            token = token or -1
            while token:
                # The only time we do a GET request to first page is
                # when sort_type and score are default values.
                if token == -1 and not sort_type and not score:
                    response = cls._do_get_app_details(app_id, lang)
                    reviews, token = parsers.reviews_first_page(response.text)
                else:
                    form_next_page = forms.reviews_next_page(
                        app_id, None if token == -1 else token, 
                        review_size, sort_type, score
                    )
                    response = cls._do_post_next_reviews(form_next_page, lang)
                    reviews, token = parsers.reviews_next_page(response.text)
                
                yield {
                    'reviews': reviews,
                    'continue': {
                        'app_id': app_id,
                        'lang': lang,
                        'review_size': review_size,
                        'sort_type': sort_type,
                        'score': score,
                        'token': token
                    }
                }
                
                time.sleep(pagination_delay)
        except GeneratorExit:
            return
        except requests.exceptions.RequestException as e:
            logging.exception(e)
        except Exception as e:
            logging.exception(e)
            logging.error('Unexpected end.')

    @classmethod
    def _do_get_review_history(cls, form):
        url = 'https://play.google.com/_/PlayStoreUi/data/batchexecute'

        return requests.post(
            url, headers=headers.POST, data=form,
            timeout=cls.TIMEOUT
        )

    @classmethod
    def review_history(cls, app_id, review_id):
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
            response = cls._do_get_review_history(form)
            return parsers.review_history(response.text)
        except:
            return None