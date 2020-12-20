import json
import re
import requests
import time

from bs4 import BeautifulSoup
from datetime import datetime

from ..helpers import list_get


class GPApp:
    TIMEOUT = 30

    @classmethod
    def _do_get_details(
        cls, id, hl='es', gl='US', *args, **kwargs
    ):
        """Gets app details and portion of reviews.

        Parameters
        ----------
        id : str
            Url parameter (Application identification).
        hl : str
            Url parameter.
        gl : str
            Url parameter.
        show_all_reviews : str
            Url parameter.

        Returns
        -------
        requests.Response (object)
        """
        url = 'https://play.google.com/store/apps/details'
        params = {
            'id': id,
            'hl': hl,
            'gl': gl,
            'showAllReviews': True
        }
        headers = {
            'Host': 'play.google.com',
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:83.0) Gecko/20100101 Firefox/83.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
        print('_do_get')

        return requests.get(
            url, params=params, headers=headers, timeout=cls.TIMEOUT,
            *args, **kwargs
        )
        # reviews, next_page_token = cls._parse_from_get(response.text)

        # return (reviews, cls._next_page_form(id, next_page_token, **kwargs))

    @classmethod
    def _parse(cls, response):
    	return {}

    @classmethod
    def scrape(cls, id, *args, **kwargs):
    	response = cls._do_get_details(id, *args, **kwargs)
    	return cls._parse(response.text)

