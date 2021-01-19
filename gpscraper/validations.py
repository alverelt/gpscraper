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
