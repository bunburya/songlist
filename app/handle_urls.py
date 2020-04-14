#!/usr/bin/env python3

"""Small helper script to add in extra fields
to song data already stored.
"""

from json import load, dump, dumps
from urllib.parse import urlparse, quote_plus

fname = 'songs.json'

with open(fname, 'r') as f:
    data = load(f)

for song in data[0]:
    url = song['url']
    song['url_escaped'] = quote_plus(url)
    song['domain'] = urlparse(url).netloc
    if 'sanitised' in song:
        del song['sanitised']

with open(fname, 'w') as f:
    dump(data, f, indent=4)

