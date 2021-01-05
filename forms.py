import json


class Sort:
    MOST_RELEVANT = None
    NEWEST = 2
    RATING = 3


def reviews_next_page(id, next_page_token, review_size, sort_type, sort_score):
    if not next_page_token:
        return None

    if sort_type in [Sort.MOST_RELEVANT, Sort.NEWEST, Sort.RATING]:
        sort_type = json.dumps(sort_type)
    else:
        sort_type = json.dumps(Sort.MOST_RELEVANT)

    if isinstance(sort_score, int) and 1 <= sort_score <= 5:
        sort_score = f'[null,{sort_score}]'
    else:
        sort_score = '[]'

    long_data = (
        f'[null,null,[2,{sort_type},[{review_size},null,'
        f'"{next_page_token}"],null,{sort_score}],["{id}",7]]'
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