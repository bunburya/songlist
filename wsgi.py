import sys

print(sys.version_info)

from app.songlist import app

if __name__ == '__main__':
    print('test')
    app.run()


