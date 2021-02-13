from bs4 import BeautifulSoup
from .general import html_script as parse_html_script
from .general import get_ds
from ..utils import list_get


def app_details(response):
    try:
        soup = BeautifulSoup(response, 'lxml')
    except:
        soup = BeautifulSoup(response, 'html.parser')

    ds = get_ds('jLZZ2e', response)
    for script in soup.find_all('script'):
        if ds in script.decode_contents():
            text = script.decode_contents()

    data = parse_html_script(text)
    data = data[0]

    parsed = {}

    parsed['title'] = list_get(data, [0, 0])

    parsed['description'] = list_get(data, [10, 0, 1])
    if parsed['description'] is not None:
        parsed['description'] = parsed['description'].replace('<br>', '\n')

    parsed['screenshots'] = []
    for ss in list_get(data, [12, 0]) or []:
        parsed['screenshots'].append(ss[3][2])

    parsed['icon'] = list_get(data, [12, 1, 3, 2])

    parsed['additional_info'] = {
        'offered_by': list_get(data, [12, 5, 1]),
        'developer': {
            'site': list_get(data, [12, 5, 3, 5, 2]),
            'mailto': list_get(data, [12, 5, 2, 0]),
            'more_apps': list_get(data, [12, 5, 5, 4, 2]),
            'privacy_policy': list_get(data, [12, 7, 2]),
            'address': list_get(data, [12, 5, 4, 0])
        },
        'installs': list_get(data, [12, 9]),
        'content_rating': [list_get(data, [12, 4, 0])],
        'interactive_elements': list_get(data, [12, 4, 3, 1]),
        'in_app_products': list_get(data, [12, 12, 0])
    }
    content_rating = list_get(data, [12, 4, 2])
    if isinstance(content_rating, list) and len(content_rating) > 1:
        for item in content_rating[1:]:
            parsed['additional_info']['content_rating'].append(item)

    parsed['editors_choice'] = bool(list_get(data, [12, 15, 0]))

    parsed['whats_new'] = list_get(data, [12, 6, 1])
    if parsed['whats_new'] is not None:
        parsed['whats_new'] = parsed['whats_new'].replace('<br>', '\n')

    parsed['category'] = list_get(data, [12, 13, 0, 2])
    parsed['released'] = list_get(data, [12, 36])

    parsed['esrb'] = {
        'description': list_get(data, [12, 4, 0]),
        'icon': list_get(data, [12, 4, 7, 3, 2])
    }

    ds = get_ds('MLWfjd', response)
    for script in soup.find_all('script'):
        if ds in script.decode_contents():
            text = script.decode_contents()

    data = parse_html_script(text)

    parsed['rating_value'] = list_get(data, [0, 6, 0])
    parsed['histogram'] = {
        '1': list_get(data, [0, 6, 1, 1, 1]),
        '2': list_get(data, [0, 6, 1, 2, 1]),
        '3': list_get(data, [0, 6, 1, 3, 1]),
        '4': list_get(data, [0, 6, 1, 4, 1]),
        '5': list_get(data, [0, 6, 1, 5, 1]),
    }
    parsed['rating_count'] = list_get(data, [0, 6, 2, 1])

    return parsed