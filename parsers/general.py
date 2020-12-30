import json
import re


def html_script(text):
    # Beware of spaces, note that between isError and false, exist 2 spaces
    regex = re.compile(r"key: 'ds:\d+', isError:  false , hash: '\d+', data:")
    init = regex.search(text).end()
    regex = re.compile(r", sideChannel: \{\}\}\);")
    end = regex.search(text).start() - 1
    return json.loads(text[init:end])