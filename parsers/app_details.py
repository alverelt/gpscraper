from bs4 import BeautifulSoup
from .general import html_script as parse_html_script
from ..helpers import list_get


def app_details(response):
    try:
        soup = BeautifulSoup(response, 'lxml')
    except:
        soup = BeautifulSoup(response, 'html.parser')

    script = soup.find_all('script')[22]
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

    script = soup.find_all('script')[23]
    text = script.decode_contents()
    data = parse_html_script(text)

    parsed['rating_value'] = list_get(data, [0, 6, 0])
    parsed['rating_stars'] = {
        '1': list_get(data, [0, 6, 1, 1, 1]),
        '2': list_get(data, [0, 6, 1, 2, 1]),
        '3': list_get(data, [0, 6, 1, 3, 1]),
        '4': list_get(data, [0, 6, 1, 4, 1]),
        '5': list_get(data, [0, 6, 1, 5, 1]),
    }
    parsed['rating_count'] = list_get(data, [0, 6, 2, 1])

    return parsed