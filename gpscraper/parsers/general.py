"""All functions functions must be common in all files in this folder."""
import json
import re


def html_script(text):
    # Beware of spaces, note that between isError and false, exist 2 spaces
    regex = re.compile(r"key:\s*'ds:\d+',\s*isError:\s*false\s*,\s*hash:\s*'\d+',\s*data:")
    init = regex.search(text).end()
    regex = re.compile(r",\s*sideChannel:\s*\{\}\}\);")
    end = regex.search(text).start() - 1
    return json.loads(text[init:end])


def get_ds(id, text):
	return re.findall(r"'(ds:\d+)' : {id:'" + id + "'", text)[-1]


def get_data(id, text, soup):
    ds = get_ds(id, text)
    for script in soup.find_all('script'):
        if ds in script.decode_contents():
            text = script.decode_contents()

    return html_script(text)