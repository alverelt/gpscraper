from bs4 import BeautifulSoup
from datetime import datetime
from .general import get_data
from ..utils import list_get

import json
import re


def search_list(data):
    _search_list = []
    for d in data[0][1][0][0][0]:
        try:
            app = {}

            app['app_pic'] = list_get(d, [1, 1, 1, 3, 2])
            app['title'] = list_get(d, [2])
            app['offered_by'] = list_get(d, [4, 0, 0, 0])
            app['developer'] = {
                'more_apps': list_get(d, [4, 0, 0, 1, 4, 2])
            }
            app['description'] = list_get(d, [4, 1, 1, 1, 1])
            app['score'] = list_get(d, [6, 0, 2, 1])
            app['app_id'] = list_get(d, [12, 0])

            _search_list.append(app)
        except:
            pass

    return _search_list


def search_list_first_page(response):
    try:
        soup = BeautifulSoup(response, 'lxml')
    except:
        soup = BeautifulSoup(response, 'html.parser')
    
    data = get_data('lGYRle', response, soup)
    _search_list = search_list(data)

    return _search_list
