import json
import re


def html_script(text):
    # Beware of spaces, note that between isError and false, exist 2 spaces
    regex = re.compile(r"key:\s*'ds:\d+',\s*isError:\s*false\s*,\s*hash:\s*'\d+',\s*data:")
    init = regex.search(text).end()
    regex = re.compile(r",\s*sideChannel:\s*\{\}\}\);")
    end = regex.search(text).start() - 1
    return json.loads(text[init:end])