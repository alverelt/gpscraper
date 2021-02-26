from enum import Enum

import json


class SortType(Enum):
    MOST_RELEVANT = None
    NEWEST = 2
    RATING = 3


def reviews_next_page(app_id, token, review_size, sort_type, rating):
    if not token:
        token = json.dumps(None)
    else:
        token = f'"{token}"'

    sort_type = json.dumps(sort_type.value)

    if 1 <= rating <= 5:
        rating = f'[null,{rating}]'
    else:
        # By default, Google Play shows reviews of all ratings.
        rating = '[]'

    long_data = (
        f'[null,null,[2,{sort_type},[{review_size},null,'
        f'{token}],null,{rating}],["{app_id}",7]]'
    )

    form = {
        'f.req': [[[
            'UsvDTd',
            long_data,
            None,
            'generic'
        ]]]
    }

    form['f.req'] = json.dumps(form['f.req'], separators=(',', ':'))
    return form


def review_history(app_id, review_id):
    # It looks like 40 is the review_size but it doesnt matter
    # because we wont be iterating through a long review history.
    long_data = (
        f'[null,null,[4,null,[40]],["{app_id}",7],"{review_id}"]'
    )

    form = {
        'f.req': [[[
            'UsvDTd',
            long_data,
            None,
            '1'
        ]]]
    }

    form['f.req'] = json.dumps(form['f.req'], separators=(',', ':'))
    return form