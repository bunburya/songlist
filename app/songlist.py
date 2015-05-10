from sys import path
path.append('/usr/local/lib/python3.4/dist-packages')

from os.path import dirname, join
from datetime import datetime
from json import dumps
from random import choice
from urllib.parse import quote_plus, urlparse
from flask import (Flask, render_template, request, flash, redirect,
                    url_for)
from .songhandler import SongList
from .atom import gen_feed

SONGFILE = join(dirname(__file__), 'songs.json')

songlist = SongList(SONGFILE)

app = Flask(__name__, static_url_path='')

@app.route('/songlist/')
def main():
    return render_template('index.html', songlist=songlist)
    
@app.route('/songlist/add', methods=['POST'])
def add_song():
    url = request.form.get('url', None)
    domain = urlparse(url).netloc
    # Remove trailing port number, if present
    colon_i = domain.find(':')
    if colon_i >= 0:
        domain = domain[:colon_i]
    song = {
        'id':           songlist.new_id(),
        'url':          url,
        'domain':       domain,
        'sanitised':    quote_plus(url),
        'title':        request.form.get('title', None),
        'other':        request.form.get('other', None), 
        'submitter':    request.form.get('submitter'),
        'time':         tuple(datetime.utcnow().timetuple())
        }
    if not (song['url'].startswith('http://') or song['url'].startswith('https://')):
        song['url'] = 'http://' + song['url']
    songlist.add_song(song, rm_old=True)
    if request.form.get('from') == 'webpage':
        return redirect('/songlist')
    else:
        return str(song['id'])

@app.route('/songlist/delete', methods=['POST'])
def del_song():
    song_id = int(request.form.get('song_id'))
    print(song_id)
    songlist.remove_song(song_id)
    if request.form.get('from') == 'webpage':
        return redirect('/songlist')
    else:
        return '1'

@app.route('/songlist/random', methods=['GET', 'POST'])
def get_song():
    uname = request.form.get('submitter')
    if uname:
        pool = list(filter(lambda d: d['submitter'] == uname, songlist.songlist))
    else:
        pool = songlist.songlist
    if pool:
        return dumps(choice(pool))
    else:
        return '0'

@app.route('/songlist/feed.atom')
def get_feed():
    feed = gen_feed(request.url, request.url_root, songlist)
    return feed.get_response()

