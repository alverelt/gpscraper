from bs4 import BeautifulSoup


def parse_app_details(response):
    soup = BeautifulSoup(response, 'html.parser')
    parsed = {}

    soup_title = soup.find('title', {'id': 'main-title'})
    parsed['title'] = soup_title.decode_contents() if soup_title else None

    return {}