def get_data(songlist, keyword):
    """Return a set of all values associated with the given keyword in
    any song entry.
    """
    s = set()
    for song in songlist:
        s.add(song[keyword])
    return s

def get_songs(songlist, **kwargs):
    """Takes a number of arguments in the form `kw=[opt1, opt2 ...]`.
    Returns the results that ANY of the options specified for EACH kw.
    """
    results = []
    for song in songlist:
        match = True
        for c in kwargs:
            if not song[c] in kwargs[c]:
                match = False
                break
        if match:
            results.append(song)
    return results
