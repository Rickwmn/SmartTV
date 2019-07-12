import weather
from gi.repository import Gtk, Gio
from sys import argv
from os import system, path
from views import LeftBar, MainStack, MoviePreview, ListTile
from utils import getCardImg, Action, Movie, getMovies, switchStack
from screeninfo import get_monitors
from requests import get
import sqlite3


connection = sqlite3.connect("./settings/data.db")
cursor = connection.cursor()
cursor.execute("SELECT * FROM Data WHERE username=\"{}\"".format(argv[1]))
settings = cursor.fetchone()


LEFT_BAR_WIDTH = settings[10]
CACHE_FOLDER = "./cache"
FNAME = "placeholder.png"
TESTMODE = False


class WeatherBox(Gtk.Grid):
    def __init__(self):
        Gtk.Grid.__init__(self)
        curWeather = weather.Weather(
            settings[4], settings[7], testMode=TESTMODE)
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
        if settings[4] == "metric":
            me = "C"
        else:
            me = "F"
        label.set_markup(
            '<big><big><big><b>{}</b></big></big></big>'.format(str(curWeather.temperature)+chr(176)+me))
        self.attach(label, 0, 1, 1, 1)


class MovieItem(Gtk.Button):
    def __init__(self, movie, width=230, heigth=345, force_wrap=False):
        Gtk.Button.__init__(self)
        self.movie = movie
        self.box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.label = Gtk.Label()
        self.label.set_line_wrap(True)
        self.label.set_justify(Gtk.Justification.CENTER)
        if force_wrap:
            if len(movie.getTitle()) > 31:
                self.label.set_label(movie.getTitle()[:28]+"...")
            else:
                self.label.set_label(movie.getTitle())
        else:
            self.label.set_label(movie.getTitle())
        self.label.set_valign(Gtk.Align.START)
        fname = "./cache/cover-medium="+movie.getTitle()+".png"
        self.box.pack_start(getCardImg(
            url=movie.getCovers()[1], fname=fname, width=width, heigth=heigth), False, False, 2)
        self.box.pack_start(self.label, False, False, 2)
        self.add(self.box)

    def onClick(self):
        window = MoviePreview(self.movie)
        window.fullscreen()
        window.connect("destroy", Gtk.main_quit)
        window.show_all()
        Gtk.main()


class Category(Gtk.Box):
    def __init__(self, category, items, width=230, heigth=345):
        Gtk.Box.__init__(
            self, orientation=Gtk.Orientation.VERTICAL, spacing=2)
        self.title = Gtk.Label(label=category)
        self.title.set_halign(Gtk.Align.START)
        self.pack_start(self.title, False, False, 10)
        self.view = Gtk.ScrolledWindow()
        self.view.set_policy(Gtk.PolicyType.AUTOMATIC,
                             Gtk.PolicyType.NEVER)
        self.pack_end(self.view, True, True, 0)

        self.grid = Gtk.Grid(
            orientation=Gtk.Orientation.HORIZONTAL)
        self.grid.set_column_spacing(6)
        self.grid.set_column_homogeneous(True)
        for i, j in enumerate(items):
            app_item = MovieItem(j, width=width, heigth=heigth)
            app_item.connect("clicked", lambda x: x.onClick())
            self.grid.attach(app_item, i, 0, 1, 1)
        self.view.add(self.grid)


class Trending(Gtk.ScrolledWindow):
    def __init__(self):
        Gtk.ScrolledWindow.__init__(self)
        categories = {
            "      New Movies": getMovies(get("https://yts.lt/api/v2/list_movies.json?sort_by=year&minimum_rating=7&limit=12").text),
        }
        self.set_policy(
            Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        self.listview = Gtk.ListBox()
        self.listview.set_selection_mode(0)
        for i, j in enumerate(categories.keys()):
            self.listview.insert(
                Category(j, categories[j], 230, 345), i+1)
        self.add(self.listview)


class Movies(Gtk.Box):
    def __init__(self):
        Gtk.Box.__init__(self, spacing=2, orientation=Gtk.Orientation.VERTICAL)
        self.movies = getMovies(
            get("https://yts.lt/api/v2/list_movies.json?sort_by=year&minimum_rating=6&limit=30").text)
        self.flowbox = Gtk.FlowBox()
        self.flowbox.set_column_spacing(6)
        self.flowbox.set_homogeneous(True)
        for j in self.movies:
            app_item = MovieItem(j, width=230, heigth=345, force_wrap=True)
            app_item.connect("clicked", lambda x: x.onClick())
            self.flowbox.add(app_item)

        # self.pack_start(self.search_bar, False, False, 0)
        self.view = Gtk.ScrolledWindow()
        self.view.set_policy(
            Gtk.PolicyType.NEVER, Gtk.PolicyType.ALWAYS)
        self.pack_start(self.view, True, True, 0)
        self.view.add(self.flowbox)


class MainWindow(Gtk.Window):
    def __init__(self):
        self.main_view = MainStack(
            [
                Trending(),
                Gtk.Label(label="Apps"),
                Movies(),
                Gtk.Label(label="Songs"),
                Gtk.Label(label="Files"),
            ])
        left_bar_actions = [
            Action("Trending", "go-home", lambda:switchStack(0, self.main_view)),
            Action("Apps", "view-grid", lambda: switchStack(1, self.main_view)),
            Action("Movies", "media-tape",
                   lambda: switchStack(2, self.main_view)),
            Action("Songs", "media-optical-cd-audio",
                   lambda: switchStack(3, self.main_view)),
            Action("Files", "folder", lambda: switchStack(4, self.main_view)),
            # Action("Settings", "open-menu",
            #        lambda: system("python3 " + path.abspath("settings.py") + " " + argv[1])),
        ]
        Gtk.Window.__init__(self, title="SmartTV OpenSource")
        self.set_default_size(get_monitors()[0].width,get_monitors()[0].height)
        self.main_divider = Gtk.Box(spacing=6)
        self.add(self.main_divider)
        self.leftbar = LeftBar(
            actions=left_bar_actions, left_bar_width=LEFT_BAR_WIDTH)
        self.sidebar_divider = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL, spacing=6)

        self.sidebar_divider.pack_start(WeatherBox(), False, False, 0)
        self.sidebar_divider.pack_start(self.leftbar, True, True, 0)
        settings_list = Gtk.ListBox()
        settings_list.set_selection_mode(Gtk.SelectionMode.NONE)
        settings_list.insert(ListTile("Settings","open-menu"),0)
        settings_list.connect("row-activated",lambda x,y:system("python3 " + path.abspath("settings.py") + " " + argv[1]))

        self.sidebar_divider.pack_end(settings_list,False,False,0)
        

        self.main_divider.pack_start(self.sidebar_divider, False, False, 0)

        self.main_divider.pack_end(self.main_view, True, True, 0)


window = MainWindow()
window.fullscreen()
window.connect("destroy", Gtk.main_quit)
window.show_all()
Gtk.main()
