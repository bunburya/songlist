def get_data(songlist, *keywords):
    """Return a set of all values associated with the given keyword in
    any song entry.
    """
    data = {kw: set() for kw in keywords}
    for song in songlist:
        for kw in keywords:
            try:
                data[kw].add(song[kw])
            except KeyError:
                continue
    # Convert sets back to lists, so they can be jsonified
    return {k: list(v) for k, v in data.items()}

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
