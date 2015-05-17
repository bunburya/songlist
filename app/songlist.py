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
from .search import get_data, get_songs

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
        'url_escaped':  quote_plus(url),
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
 
@app.route('/songlist/search', methods=['GET'])
def search():
    # NOTE: Using semicolons to separate params in GET queries
    # works for present purposes because the params we're using
    # (domain and submitter) are unlikely to contain semicolons.
    # It isn't really a long-term sustainable solution, unless
    # all params are escaped first.
    args = request.args.copy()
    targ = args.pop('target', None)
    if targ == 'songs':
        return dumps(get_songs(songlist,
                    **{kw: val.split(';') for kw, val in args.items()}))
    elif targ == 'data':
        return dumps(get_data(songlist,
                                *args.get('data', '').split(';')))
    else:
        return '0'

@app.route('/play')
def play():
    submitters = get_data(songlist, 'submitter')
    return render_template('play.html', submitters=submitters)
