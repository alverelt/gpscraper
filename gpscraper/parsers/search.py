from bs4 import BeautifulSoup
from datetime import datetime
from ..utils import list_get

import json
import logging
import re


logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s', 
    level=logging.INFO
)

def html_script(text):
    regex = re.compile(
        r"key:\s*'ds:3',\s*isError:\s*false\s*,\s*hash:\s*'6',\s*data:"
        "(.*)"
        r",\s*sideChannel:\s*\{\}\}\);"
    )
    found = regex.search(text)

    try:
        return json.loads(found.group(1))
    except json.JSONDecodeError:
        logging.error('Body content could not be parsed to dict.')
        return []


def get_ds(id, text):
	return re.findall(r"'(ds:\d+)' : {id:'" + id + "'", text)[-1]


def get_data(id, text, soup):
    try:
        ds = get_ds(id, text)
    except IndexError:
        logging.error(f'Not found {id}.')
        return []

    text = None   
    for script in soup.find_all('script'):
        if ds in script.decode_contents():
            text = script.decode_contents()

    if text is None:
        logging.error(f'Not found {ds} as a key in any script tag.')
        return []

    return html_script(text)


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
    results = search(list_get(data, [0, 1, 0, 0, 0], []))

    token = list_get(data, [0, 1, 0, 0, 7, 1])

    response = response.replace('\\n', '')
    regex = re.compile(r'"QEwZ9c":"%\.@\.(.*)\]","QrtxK"')
    unknown_1 = regex.search(response).group(1)

    return results, token, unknown_1


def search_next_page(response):
    response = re.sub(r'(\\\\n|\\n)', '', response)

    regex = re.compile(r'\[\["wrb.fr')
    init = regex.search(response).start()

    try:
        data = json.loads(response[init:])
        data = json.loads(data[0][2])
    except (json.JSONDecodeError, TypeError):
        logging.error('Could not parse next searches.')
        return [], None

    results = search(list_get(data, [0, 0, 0], []))

    token = list_get(data, [0, 0, 7, 1])

    return results, token
