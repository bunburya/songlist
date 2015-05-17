#!/usr/bin/env python3

import sys

print(sys.version_info)

from app.songlist import app

if __name__ == '__main__':
    if '--debug' in sys.argv:
        app.debug = True
    app.run()


