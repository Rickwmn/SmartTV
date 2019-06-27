import weather
from gi.repository import Gtk, Gdk, Gio
from sys import argv
from os import system, path
from views import LeftBar
from utils import getCardImg, Action, Movie, getMovies
from requests import get
from math import ceil, floor
import sqlite3

connection = sqlite3.connect("./settings/data.db")
cursor = connection.cursor()
cursor.execute("SELECT * FROM Data WHERE username=\"{}\"".format(argv[1]))
settings = cursor.fetchone()


LEFT_BAR_WIDTH = settings[9]
CACHE_FOLDER = "./cache"
FNAME = "placeholder.png"
TESTMODE = True


class WeatherBox(Gtk.Grid):
    def __init__(self):
        Gtk.Grid.__init__(self)
        curWeather = weather.Weather(testMode=TESTMODE)
        condition = curWeather.iconCode
        conditions = {"01d": "weather-clear",
                      "02d": "weather-few-clouds",
                      "03d": "weather-overcast",
                      "04d": "weather-overcast",
                      "09d": "weather-showers",
                      "10d": "weather-showers-scattered",
                      "11d": "weather-storm",
                      "13d": "weather-snow",
                      "50d": "weather-fog",
                      "01n": "weather-clear-night",
                      "02n": "weather-few-clouds-night",
                      "03n": "weather-overcast",
                      "04n": "weather-overcast",
                      "09n": "weather-showers",
                      "10n": "weather-showers-scattered",
                      "11n": "weather-storm",
                      "13n": "weather-snow",
                      "50n": "weather-fog"}
        icon = Gio.ThemedIcon(name=conditions[condition])
        image = Gtk.Image.new_from_gicon(icon, 6)
        image.set_pixel_size(LEFT_BAR_WIDTH-4)
        image.set_halign(Gtk.Align.CENTER)
        self.add(image)
        label = Gtk.Label()
        label.set_markup(
            '<big><big><big><b>{}</b></big></big></big>'.format(str(curWeather.temperature)+"°C"))
        self.attach(label, 0, 1, 1, 1)


class AppItem(Gtk.Grid):
    def __init__(self, name, image, width=300, heigth=150):
        Gtk.Grid.__init__(self)
        self.label = Gtk.Label()
        self.label.set_line_wrap(True)
        self.label.set_justify(Gtk.Justification.CENTER)
        self.label.set_label(name)
        self.label.set_valign(Gtk.Align.START)
        self.attach(getCardImg(
            url=image, fname=FNAME, testMode=TESTMODE, width=width, heigth=heigth), 0, 0, 1, 1)
        self.attach(self.label, 0, 1, 1, 1)


class Category(Gtk.Box):
    def __init__(self, category, items, width=300, heigth=150):
        Gtk.Box.__init__(
            self, orientation=Gtk.Orientation.VERTICAL, spacing=2)
        self.title = Gtk.Label(label=category)
        self.title.set_halign(Gtk.Align.START)
        self.pack_start(self.title, False, False, 10)
        self.view = Gtk.ScrolledWindow()
        self.view.set_policy(Gtk.PolicyType.AUTOMATIC,
                             Gtk.PolicyType.NEVER)
        self.pack_end(self.view, True, True, 0)
        self.flowbox = Gtk.FlowBox(
            orientation=Gtk.Orientation.HORIZONTAL)
        self.flowbox.set_min_children_per_line(7)
        self.flowbox.set_homogeneous(True)

        for i, j in enumerate(items):
            self.flowbox.insert(
                AppItem(j.getTitle(), j.getCovers()[1], width=width, heigth=heigth), i+1)
        self.view.add(self.flowbox)


class MainBar(Gtk.ScrolledWindow):
    def __init__(self):
        Gtk.ScrolledWindow.__init__(self)
        categories = {
            "      Top Movies": getMovies(get("https://yts.lt/api/v2/list_movies.json?sort_by=download_count&minimum_rating=8&limit=7").text),
        }
        self.set_policy(
            Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        self.listview = Gtk.ListBox()
        self.listview.set_selection_mode(0)
        for i, j in enumerate(categories.keys()):
            self.listview.insert(
                Category(j, categories[j], 230, 345), i+1)
        self.add(self.listview)


class MainWindow(Gtk.Window):
    def __init__(self):
        left_bar_actions = [
            Action("Trending", "go-home", lambda:0),
            Action("Apps", "view-grid", lambda: 0),
            Action("Movies", "media-tape", lambda: 0),
            Action("Files", "folder", lambda: 0),
            Action("Settings", "open-menu",
                   lambda: system("python3 " + path.abspath("settings.py") + " 300")),
        ]
        Gtk.Window.__init__(self, title="SmartTV OpenSource")
        self.set_default_size(Gdk.Screen.get_default().get_width(),
                              Gdk.Screen.get_default().get_height())
        self.main_divider = Gtk.Box(spacing=6)
        self.add(self.main_divider)
        self.leftbar = LeftBar(
            actions=left_bar_actions, left_bar_width=LEFT_BAR_WIDTH, start_index=1, ignore_start=1)
        self.leftbar.listview.insert(WeatherBox(), 0)
        self.main_divider.pack_start(self.leftbar, False, True, 0)
        self.main_divider.pack_end(MainBar(), True, True, 0)


window = MainWindow()
window.fullscreen()
window.connect("destroy", Gtk.main_quit)
window.show_all()
Gtk.main()
