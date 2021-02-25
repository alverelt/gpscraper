from bs4 import BeautifulSoup
from datetime import datetime
from .general import get_data
from ..utils import list_get

import json
import re


def search(data):
    results = []
    for d in data:
        try:
            app = {}

            app['icon'] = list_get(d, [1, 1, 1, 3, 2])
            app['title'] = list_get(d, [2])
            app['offered_by'] = list_get(d, [4, 0, 0, 0])
            app['developer'] = {
                'more_apps': list_get(d, [4, 0, 0, 1, 4, 2])
            }
            app['description'] = list_get(d, [4, 1, 1, 1, 1])
            app['rating'] = list_get(d, [6, 0, 2, 1])
            app['app_id'] = list_get(d, [12, 0])

            results.append(app)
        except:
            pass

    return results


def search_first_page(response):
    try:
        soup = BeautifulSoup(response, 'lxml')
    except:
        soup = BeautifulSoup(response, 'html.parser')
    
    data = get_data('lGYRle', response, soup)
    results = search(data[0][1][0][0][0])

    token = list_get(data, [0, 1, 0, 0, 7, 1])

    response = response.replace('\\n', '')
    regex = re.compile(r'"QEwZ9c":"%\.@\.(.*)\]","QrtxK"')
    strange_data = regex.search(response).group(1)

    return results, token, strange_data


def search_next_page(response):
    response = response.replace('\\n', '').replace('\n', '')

    regex = re.compile(r'\[\["wrb.fr')
    init = regex.search(response).start()

    data = json.loads(response[init:])
    data = json.loads(data[0][2])

    results = search(data[0][0][0])

    return results
