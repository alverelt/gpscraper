from .general import get_data
from ..utils import list_get

import json
import logging
import re


logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s', 
    level=logging.INFO
)


def permissions(response):
    text = re.search(r'"xdSrCf","(.*)\\n",null,null', response).group(1)

    try:
        data = json.loads(text.replace('\\n', '').replace('\\"', '"'))
    except (json.JSONDecodeError, TypeError):
        logging.error('Could not parse permissions.')
        return []

    results = []

    for d in data[0]:
        perm = {}

        perm['access'] = list_get(d, [0])
        perm['icon'] = list_get(d, [1, 3, 2])
        perm['details'] = [
            list_get(detail, [1]) 
            for detail in list_get(d, [2]) or []
        ] 

        results.append(perm)
       
    return results