def id(value):
    if not isinstance(value, str):
        raise TypeError('Id must be of type str.')
    if not value:
        raise ValueError('Id cannot be empty.')

def lang(value):
    if not isinstance(value, str):
        raise TypeError('Lang must be of type str.')
    if not value:
        raise ValueError('Lang cannot be empty.')

def review_size(value):
    if not isinstance(value, int):
        raise TypeError('Review size must be of type int.')

    if value < 1:
        raise ValueError('Review size can not be less than 1.')

def sort_type(data):
    pass