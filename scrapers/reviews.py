import json
import re
import requests
import time

from bs4 import BeautifulSoup
from datetime import datetime

from ..helpers import list_get


class GPReviews:
    TIMEOUT = 30

    @classmethod
    def _do_get_reviews(
        cls, id, hl='es', gl='US', *args, **kwargs
    ):
        """Get portion of all reviews.

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
        **kwargs:
            Optional params for _next_page_form method.

        Returns
        -------
        tuple -> (list, dict | None)
            [0] List of current response reviews.
            [1] Required info for pagination.
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

        response = requests.get(
            url, params=params, headers=headers, timeout=cls.TIMEOUT
        )
        reviews, next_page_token = cls._parse_from_get(response.text)

        return (reviews, cls._next_page_form(id, next_page_token, **kwargs))

    @classmethod
    def _do_post_reviews(cls, id, next_page_form, hl='es', *args, **kwargs):
        """Get portion of all reviews.

        Parameters
        ----------
        id : str
            Url parameter (Application identification).
        hl : str
            Url parameter.
        **kwargs:
            Optional params for _next_page_form method.

        Returns
        -------
        tuple -> (list, dict | None)
            [0] list of current response reviews.
            [1] info required for next page.
        """
        url = 'https://play.google.com/_/PlayStoreUi/data/batchexecute'
        params = {
            'hl': hl
        }

        headers = {
            'Host': 'play.google.com',
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:83.0) Gecko/20100101 Firefox/83.0',
            'Accept': '*/*',
            'Accept-Language': 'es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate, br',
            'Referer': 'https://play.google.com/',
            'X-Same-Domain': '1',
            'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8',
            'Origin': 'https://play.google.com',
            'DNT': '1',
            'Connection': 'keep-alive',
            'TE': 'Trailers',
        }

        response = requests.post(
            url, params=params, headers=headers, data=next_page_form,
            timeout=cls.TIMEOUT
        )
        reviews, next_page_token = cls._parse_from_post(response.text)

        review_size = kwargs.pop('review_size', None)
        return (
            reviews,
            cls._next_page_form(id, next_page_token, review_size=review_size)
        )

    @classmethod
    def scrape(cls, id, pagination_delay=2, *args, **kwargs):
        """Generator, gets all reviews.

        Parameters
        ----------
        id : str
            Url parameter (Application identification).
        pagination_delay : int | float
            Time between each scrape.
        **kwargs:
            Optional params for _do_get_reviews, _do_post_reviews
            and _next_page_form methods.

        Yields
        ------
        list of dict
        """
        try:
            reviews, next_page_form = cls._do_get_reviews(id, *args, **kwargs)
            yield reviews

            if next_page_form:
                finished = False
                while not finished:
                    time.sleep(pagination_delay)
                    reviews, next_page_form = cls._do_post_reviews(
                        id, next_page_form, *args, **kwargs
                    )

                    yield reviews

                    finished = not bool(next_page_form)
        except:
            print('Unexpected end.')
            pass
        finally:
            print(
                'End of scrape, if your list is empty, please try again.'
            )

    @classmethod
    def _parse(cls, data):
        reviews = []
        for d in data[0]:
            try:
                review = {}

                review['score'] = list_get(d, [2])
                review['name'] = list_get(d, [1, 0])
                review['comment'] = list_get(d, [4])
                review['reply'] = list_get(d, [7, 1])
                review['version'] = list_get(d, [10])
                review['epoch'] = list_get(d, [5, 0])

                review['datetime'] = datetime.utcfromtimestamp(review['epoch'])
                review['datetime'] = review['datetime'].strftime('%Y-%m-%d %H:%M:%S')

                review['profile_pic'] = list_get(d, [1, 1, 3, 2])
                review['background_pic'] = list_get(d, [9, 4, 3, 2])
                review['likes'] = list_get(d, [6])

                reviews.append(review)
            except:
                pass

        next_page_token = list_get(data, [1, 1])

        return reviews, next_page_token

    @classmethod
    def _parse_from_get(cls, response):
        try:
            soup = BeautifulSoup(response, 'lxml')
        except:
            soup = BeautifulSoup(response, 'html.parser')

        script = soup.find_all('script')[-3]
        text = script.decode_contents()

        # Beware of spaces, note that between isError and false, exist 2 spaces
        regex = re.compile(r"key: 'ds:\d\d', isError:  false , hash: '\d\d', data:")
        init = regex.search(text).end()

        regex = re.compile(r", sideChannel: \{\}\}\);")
        end = regex.search(text).start() - 1

        data = json.loads(text[init:end])

        return cls._parse(data)

    @classmethod
    def _parse_from_post(cls, response):
        regex = re.compile(r"\[")
        init = regex.search(response).start()

        data = json.loads(response[init:])
        data = json.loads(data[0][2])

        return cls._parse(data)

    @staticmethod
    def _next_page_form(
        package_name, next_page_token, sort_type=None, review_size=40
    ):
        if not next_page_token:
            return None

        review_size = review_size or 40

        # This should remain None, its implementation is not done yet.
        sort_type = None
        sort_type = json.dumps(sort_type)

        long_data = (
            f'[null,null,[2,{sort_type},[{review_size},null,'
            f'"{next_page_token}"],null,[]],["{package_name}",7]]'
        )
        form = {
            'f.req': [[[
                'UsvDTd',
                long_data,
                None,
                'generic'
            ]]],
            '': ''
        }

        form['f.req'] = json.dumps(form['f.req'], separators=(',', ':'))
        return form
