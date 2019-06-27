from gi.repository import Gtk, GdkPixbuf
import requests
import json


# class TorrentData


class Movie:
    def __init__(self, jsonS):
        self.json = jsonS
        self.parsed = json.loads(self.json)

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
        return self.parsed["torrents"]


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


def getImageFromWeb(url, fname, testMode=True):
    img = Gtk.Image()
    if not testMode:
        r = requests.get(url)
        with open('placeholder.png', 'wb') as outfile:
            outfile.write(r.content)
    img.set_from_file(fname)
    return img


def getCardImg(url, fname, testMode=True, width=300, heigth=150):
    getImageFromWeb(url, fname, testMode)
    return scaleImgToCard(fname, width=width, heigth=heigth)


class Action():
    def __init__(self, title, icon_name, function):
        self.function = function
        self.title = title
        self.icon_name = icon_name

    def go(self):
        self.function()
