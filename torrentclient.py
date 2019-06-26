import libtorrent as lt
import time
import sys
import urllib.request
from multiprocessing import Process
from os import remove
import os


def info(title):
    print(title)
    print('module name:', __name__)
    print('parent process:', os.getppid())
    print('process id:', os.getpid())


class Torrent:
    def __init__(self):
        self.session = lt.session()
        self.session.listen_on(6881, 6891)

    def torrent_from_file(self, location):
        self.info = lt.torrent_info(location)

    def torrent_from_url(self, url):
        headers = {}
        headers['User-Agent'] = "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:48.0) Gecko/20100101 Firefox/48.0"
        with open("temp.torrent", "wb") as file:
            req = urllib.request.Request(url, headers=headers)
            html = urllib.request.urlopen(req).read()
            file.write(html)

        self.info = lt.torrent_info("temp.torrent")
        remove("temp.torrent")

    def start(self):
        info("bla")
        self.torrent = self.session.add_torrent(
            {'ti': self.info, 'save_path': '/home/cigla/Downloads'})
        while not self.torrent.is_seed():
            self.status = self.torrent.status()
            self.state_str = [
                'queued',
                'checking',
                'downloading metadata',
                'downloading',
                'finished',
                'seeding',
                'allocating',
                'checking fastresume'
            ]
            print(self.status.progress*100)
        # s.progress * 100
        # s.download_rate / 1000
        # s.upload_rate / 1000
        # s.num_peers, state_str[s.state]
        return 0


def start():
    mytorrent = Torrent()
    mytorrent.torrent_from_url(
        "https://yts.lt/torrent/download/BCEB706EA32EDD855FCA4426DF8A7831F53CC3EE")
    mytorrent.start()


p = Process(target=start)
p.start()
while True:
    print("bla")
