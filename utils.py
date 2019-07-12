from gi.repository import Gtk, GdkPixbuf, Gio
import requests
import json
from os.path import isfile
from math import floor, ceil
import torrentclient
from multiprocessing import Process


class TorrentData:
    def __init__(self, raw_torrent_data):
        self.url = raw_torrent_data["url"]
        self.peers = raw_torrent_data["peers"]
        self.seeds = raw_torrent_data["seeds"]
        self.size = raw_torrent_data["size"]
        self.size_bytes = raw_torrent_data["size_bytes"]
        self.quality = raw_torrent_data["quality"]

    def download(self):
        p = Process(target=lambda: torrentclient.start_from_url(self.url))
        p.start()


class Movie:
    def __init__(self, jsonS):
        self.json = jsonS
        self.parsed = json.loads(self.json)

    def getTrailerCode(self):
        return self.parsed["yt_trailer_code"]

    def getId(self):
        return self.parsed["id"]

    def getUrl(self):
        return self.parsed["url"]

    def getImbdCode(self):
        return self.parsed["imdb_code"]

    def getTitle(self):
        return self.parsed["title"]

    def getTitleEn(self):
        return self.parsed["title_english"]

    def getSlug(self):
        return self.parsed["slug"]

    def getYear(self):
        return self.parsed["year"]

    def getRating(self):
        return self.parsed["rating"]

    def getGenres(self):
        return self.parsed["genres"]

    def getDescription(self):
        return self.parsed["description_full"]

    def getLanguage(self):
        return self.parsed["language"]

    def getCovers(self):
        return [self.parsed["small_cover_image"], self.parsed["medium_cover_image"], self.parsed["large_cover_image"]]

    def getTorrentData(self):
        return [TorrentData(i) for i in self.parsed["torrents"]]

    def getRuntime(self):
        return self.parsed["runtime"]


def getMovies(jsonS):
    movies = []
    for i in json.loads(jsonS)["data"]["movies"]:
        movies.append(Movie(json.dumps(i)))
    return movies


def scaleImgToCard(fname, width=300, heigth=150):
    pixbuf = GdkPixbuf.Pixbuf.new_from_file(fname)
    pixbuf = pixbuf.scale_simple(
        width, heigth, GdkPixbuf.InterpType.HYPER)
    img = Gtk.Image()
    img.set_from_pixbuf(pixbuf)
    return img


def getImageFromWeb(url, fname):
    r = requests.get(url)
    with open(fname, 'wb') as outfile:
        outfile.write(r.content)


def getStarRating(ratings):
    not_starred = 5-ceil(ratings)
    starred = floor(ratings)
    semi_starred = int(ratings) != ratings
    rating_widget = Gtk.Grid()
    layout = ["starred" for i in range(
        starred)]+["semi-starred" for i in range(semi_starred)]+["non-starred" for i in range(not_starred)]
    for i, j in enumerate(layout):
        image = Gtk.Image.new_from_icon_name(j, 3)
        rating_widget.attach(image, i, 0, 1, 1)
    return rating_widget


def switchStack(index, stack):
    stack.set_visible_child(stack.get_children()[index])
    stack.get_children()[index].show()


def getCardImg(url, fname, width=300, heigth=150):
    if not isfile(fname):
        getImageFromWeb(url, fname)

    try:
        image = scaleImgToCard(fname, width, heigth)
    except:
        getImageFromWeb(
            "https://via.placeholder.com/{}x{}.png/ffffff/000000?text=Ooops, something went wrong!".format(width, heigth), fname)
        image = scaleImgToCard(fname, width, heigth)
    return image


class Action():
    def __init__(self, title, icon_name, function):
        self.function = function
        self.title = title
        self.icon_name = icon_name

    def go(self):
        self.function()
