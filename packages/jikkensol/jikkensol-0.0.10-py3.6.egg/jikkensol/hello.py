import sys, os

class Hello:
    def __init__(self, name):
        self._name = name

    def say(self):
        print('{}さん、こんにちは。'.format(self._name))

    def song(self):
        print('バージョン 0.0.10')

        song_file = os.path.dirname(os.path.abspath(__file__)) + os.sep +\
                'files' + os.sep + 'songs.txt'
        with open(song_file, 'rt') as f:
            while True:
                line = f.readline()
                if not line:
                    break
                print(line, end='')


if __name__ == '__main__':
    h = Hello('太郎')
    h.say()
    h.song()
