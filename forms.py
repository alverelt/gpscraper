import json


def reviews_next_page(id, next_page_token, review_size, sort_type):
    if not next_page_token:
        return None

    # This should remain None, its implementation is not done yet.
    sort_type = None
    sort_type = json.dumps(sort_type)

    long_data = (
        f'[null,null,[2,{sort_type},[{review_size},null,'
        f'"{next_page_token}"],null,[]],["{id}",7]]'
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