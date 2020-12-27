from bs4 import BeautifulSoup
from datetime import datetime
from ..helpers import list_get

import json
import re


def parse_reviews(data):
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

            review['datetime'] = datetime.fromtimestamp(review['epoch'])
            review['datetime'] = review['datetime'].strftime('%Y-%m-%d %H:%M:%S')

            review['profile_pic'] = list_get(d, [1, 1, 3, 2])
            review['background_pic'] = list_get(d, [9, 4, 3, 2])
            review['likes'] = list_get(d, [6])

            reviews.append(review)
        except:
            pass

    return reviews

def parse_first_page(response):
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
    reviews = parse_reviews(data)

    next_page_token = list_get(data, [1, 1])

    return reviews, next_page_token

def parse_next_page(response):
    regex = re.compile(r"\[")
    init = regex.search(response).start()

    data = json.loads(response[init:])
    data = json.loads(data[0][2])
    reviews = parse_reviews(data)

    next_page_token = list_get(data, [1, 1])

    return reviews, next_page_token 