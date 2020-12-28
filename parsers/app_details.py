from bs4 import BeautifulSoup
from ..helpers import list_get

import json
import re


def parse_app_details(response):
    try:
        soup = BeautifulSoup(response, 'lxml')
    except:
        soup = BeautifulSoup(response, 'html.parser')

    script = soup.find_all('script')[22]
    text = script.decode_contents()

    # Beware of spaces, note that between isError and false, exist 2 spaces
    regex = re.compile(r"key: 'ds:\d+', isError:  false , hash: '\d+', data:")
    init = regex.search(text).end()
    regex = re.compile(r", sideChannel: \{\}\}\);")
    end = regex.search(text).start() - 1
    data = json.loads(text[init:end])
    data = data[0]

    parsed = {}

    parsed['title'] = list_get(data, [0, 0])

    parsed['description'] = list_get(data, [10, 0, 1])
    if parsed['description'] is not None:
        parsed['description'] = parsed['description'].replace('<br>', '\n')

    parsed['screenshots'] = []
    for ss in list_get(data, [12, 0]):
        parsed['screenshots'].append(ss[3][2])
    
    parsed['icon'] = list_get(data, [12, 1, 3, 2])
    parsed['developer'] = list_get(data, [12, 5, 1])
    parsed['mailto'] = list_get(data, [12, 5, 2])
    parsed['developer_site'] = list_get(data, [12, 5, 3, 5, 2])
    parsed['developer_apps'] = list_get(data, [12, 5, 5, 4, 2])

    parsed['whats_new'] = list_get(data, [12, 6, 1])
    if parsed['whats_new'] is not None:
        parsed['whats_new'] = parsed['whats_new'].replace('<br>', '\n')

    parsed['docs'] = list_get(data, [12, 7, 2])
    parsed['downloads'] = list_get(data, [12, 9])
    parsed['category'] = list_get(data, [12, 13, 0, 2])
    parsed['released'] = list_get(data, [12, 36])

    return parsed