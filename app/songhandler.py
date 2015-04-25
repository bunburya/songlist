from json import load, dump
from os.path import exists, dirname
from os import makedirs

from time import struct_time, strftime

class SongList:
    
    """This class basically provides a clean interface for accessing and
    manipulating the song list and handles the song file behind the
    scenes.
    """
    
    def __init__(self, fpath):
        self.songfile = fpath
        if exists(fpath):
            self.load_list()
        else:
            self._id = 0
            self.songlist = []
            self.save_list()
    
    def __iter__(self):
        """Iterate backwards through the songlist (most to least recent).
        """
        self._index = len(songlist) - 1
        return self
    
    def __next__(self):
        if self._index < 0:
            raise StopIteration
        song = self.songlist[self._index]
        self._index -= 1
        return song
    
    def save_list(self):
        fdir = dirname(self.songfile)
        if fdir and not exists(fdir):
            makedirs(fdir)
        with open(self.songfile, 'w') as f:
            dump([self.songlist, self._id], f)
    
    def load_list(self):
        with open(self.songfile, 'r') as f:
            try:
                self.songlist, self._id = load(f)
            except ValueError:
                # File is not valid JSON; just make an empty list
                self._id = 0
                self.songlist = []
                self.save_list()
                
    def add_song(self, song, rm_old=True):
        if rm_old:
            old_ids = []
            for s in songlist:
                if s['url'] == song['url']:
                    old_ids.append(s['id'])
            for _id in old_ids:
                self.remove_song(_id)
        self.songlist.append(song)
        self.save_list()
    
    def remove_song(self, song_id):
        for s in self.songlist:
            if s['id'] == song_id:
                self.songlist.remove(s)
                self.save_list()
                return
    
    def clear_list(self):
        self.songlist = []
        self.save_list()
    
    def new_id(self):
        # Each song is to be given a unique ID number to make removal
        # easy.
        self._id += 1
        return self._id
    
    def timestring(self, ttuple):
        """Take the tuple stored in the JSON file and turn it into a
        human readable string.
        """
        return strftime('%a %d/%m/%Y at %H:%M:%S %Z', struct_time(ttuple))
