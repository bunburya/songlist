from json import load, dump
from os.path import exists, dirname
from os import makedirs

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
                
    def add_song(self, song):
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
        
