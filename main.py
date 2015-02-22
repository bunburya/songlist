#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from time import strftime
from json import dumps
from random import choice
from flask import (Flask, render_template, request, flash, redirect,
                    url_for)
from songlist import SongList

SONGFILE = 'songs.json'

songlist = SongList(SONGFILE)

app = Flask(__name__)

@app.route('/')
def main():
    return render_template('index.html', songlist=songlist.songlist)
    
@app.route('/add', methods=['POST'])
def add_song():
    song = {
        'id':           songlist.new_id(),
        'url':          request.form.get('url', None),
        'title':        request.form.get('title', None),
        'other':        request.form.get('other', None), 
        'submitter':    request.form.get('submitter'),
        'time':         strftime('%d/%m/%Y, %H:%M:%S (%Z)')
        }
    if not (song['url'].startswith('http://') or song['url'].startswith('https://')):
        song['url'] = 'http://' + song['url']
    songlist.add_song(song)
    if request.form.get('from') == 'webpage':
        return redirect('/')
    else:
        return str(song['id'])

@app.route('/delete', methods=['POST'])
def del_song():
    song_id = int(request.form.get('song_id'))
    print(song_id)
    songlist.remove_song(song_id)
    if request.form.get('from') == 'webpage':
        return redirect('/')
    else:
        return '1'

@app.route('/random', methods=['GET', 'POST'])
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

if __name__ == '__main__':
    from sys import argv
    if '--debug' in argv:
        app.debug = True
    app.run()
