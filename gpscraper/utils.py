import os
import random


FILE_DIR = os.path.dirname(os.path.join(__file__))

def list_get(data, pos, default=None):
    "Access multidimensional list returning default if an exception is raised."
    for p in pos:
        try:
            data = data[p]
        except:
            data = default
            break
    return data