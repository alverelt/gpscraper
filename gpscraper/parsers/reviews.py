from bs4 import BeautifulSoup
from datetime import datetime
from .general import get_data
from ..utils import list_get

import json
import re


def reviews(data):
    reviews = []
    for d in data[0]:
        try:
            review = {}

            review['id'] = list_get(d, [0])
            review['score'] = list_get(d, [2])
            review['name'] = list_get(d, [1, 0])
            review['comment'] = list_get(d, [4])
            review['reply'] = list_get(d, [7, 1])
            review['version'] = list_get(d, [10])
            review['epoch'] = list_get(d, [5, 0])

            _datetime = datetime.fromtimestamp(review['epoch'])
            review['datetime'] = _datetime.strftime('%Y-%m-%d %H:%M:%S')

            review['profile_pic'] = list_get(d, [1, 1, 3, 2])
            review['background_pic'] = list_get(d, [9, 4, 3, 2])
            review['likes'] = list_get(d, [6])

            reviews.append(review)
        except:
            pass

    return reviews

def reviews_first_page(response):
    try:
        soup = BeautifulSoup(response, 'lxml')
    except:
        soup = BeautifulSoup(response, 'html.parser')

    data = get_data('UsvDTd', response, soup)
    _reviews = reviews(data)

    next_page_token = list_get(data, [1, 1])

    return _reviews, next_page_token

def reviews_next_page(response):
    regex = re.compile(r"\[")
    init = regex.search(response).start()

    data = json.loads(response[init:])
    data = json.loads(data[0][2])
    _reviews = reviews(data)

    next_page_token = list_get(data, [1, 1])

    return _reviews, next_page_token

def review_history(response):
    text = re.search(r'"UsvDTd","(.*)\\n",null,null', response).group(1)
    data = json.loads(text.replace('\\n', '').replace('\\"', '"'))

    histories = []

    for d in data[0]:
        history = {}

        history['id'] = list_get(d, [0])
        history['name'] = list_get(d, [1, 0])
        history['profile_pic'] = list_get(d, [9, 3, 0, 3, 2])
        history['background_pic'] = list_get(d, [9, 4, 3, 2])
        history['score'] = list_get(d, [2])
        history['comment'] = list_get(d, [4])
        history['epoch'] = list_get(d, [5, 0])

        _datetime = datetime.fromtimestamp(history['epoch'])
        history['datetime'] = _datetime.strftime('%Y-%m-%d %H:%M:%S')
        history['version'] = list_get(d, [10])

        histories.append(history)

    return histories