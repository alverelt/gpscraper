import json


class Sort:
    MOST_RELEVANT = None
    NEWEST = 2
    RATING = 3

    @classmethod
    def contains(cls, value):
        return value in [cls.MOST_RELEVANT, cls.NEWEST, cls.RATING]


def reviews_next_page(id, next_page_token, review_size, sort_type, sort_score):
    if not next_page_token:
        next_page_token = json.dumps(None)
    else:
        next_page_token = f'"{next_page_token}"'

    sort_type = json.dumps(sort_type)

    if 1 <= sort_score <= 5:
        sort_score = f'[null,{sort_score}]'
    else:
        # By default, Google Play sorts by all score.
        sort_score = '[]'

    long_data = (
        f'[null,null,[2,{sort_type},[{review_size},null,'
        f'{next_page_token}],null,{sort_score}],["{id}",7]]'
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