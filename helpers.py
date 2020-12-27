import os
import random


FILE_DIR = os.path.dirname(os.path.join(__file__))

def list_get(data, pos, default=None):
    "Access multidimensional list returning default if an exception is raised."
    for p in pos:
        try:
            data = data[p]
        except:
            data = default
            break
    return data

def load_proxy(proxies_list_path=''):
    '''Carga proxies http.'''
    import random
    if not proxies_list_path:
        proxies_dir = os.path.dirname(FILE_DIR)
        proxies_list_path = os.path.join(proxies_dir, 'HTTP-proxies.txt')

    try:
        with open(proxies_list_path) as f:
            proxies_list = f.readlines()
    except:
        proxies_list = []

    if not proxies_list:
        return {}

    return {'http': random.choice(proxies_list).strip()}