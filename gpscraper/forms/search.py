import json


def search_next_page(token, strange_data):
    long_data = (
        f'[[null,[{strange_data}],null,"{token}"]]'
    )

    form = {
        'f.req': [[[
            'qnKhOb',
            long_data,
            None,
            'generic'
        ]]]
    }

    form['f.req'] = json.dumps(form['f.req'], separators=(',', ':'))
    return form