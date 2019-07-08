from gi.repository import Gtk, Gio, Gdk
from utils import getCardImg, getStarRating
from screeninfo import get_monitors
from math import ceil, floor


# class LoadingScreen(Gtk.Window):
#     def __init__(self, function, args=()):
#         Gtk.Window.__init__(self, title="SmartTV OpenSource")
#         self.box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
#         self.box.set_hexpand(True)
#         self.box.set_vexpand(True)
#         self.box.pack_start(getCardImg(
#             "https://proxy.duckduckgo.com/iu/?u=http%3A%2F%2Fwww.roxboroughliving.com%2Fwp-content%2Fuploads%2F2016%2F03%2Flogo-placeholder.jpg&f=1", "./cache/logo_placeholder.png", 550, 296), True, False, 18)
#         self.spinner = Gtk.Spinner()
#         self.spinner.start()
#         self.box.pack_start(self.spinner, False, False, 0)
#         self.add(self.box)
#         function(*args)


class MoviePreview(Gtk.Window):
    def __init__(self, movie):
        Gtk.Window.__init__(self, title="SmartTV OpenSource")

        height = get_monitors()[0].height
        aspect = height/750
        ratings = float(round(movie.getRating()/2, 1))

        self.movie = movie
        self.divider = Gtk.Box(spacing=18)
        self.image = getCardImg(movie.getCovers()[2], "./cache/cover-large={}".format(
            movie.getTitle())+".png", width=500*aspect, heigth=height)
        self.divider.set_hexpand(True)
        self.divider.set_vexpand(True)
        self.divider.set_margin_right(18)
        self.divider.pack_start(self.image, False, False, 0)

        self.title = Gtk.Label()
        self.title.set_markup(
            "<big><big><big><big>{}</big></big></big></big>".format(movie.getTitleEn()))
        self.title.set_hexpand(True)
        self.title.set_halign(Gtk.Align.START)

        self.desc = Gtk.Label()
        self.desc.set_markup(
            "<big><big>{}</big></big>".format(movie.getDescription()))
        self.desc.set_line_wrap(True)

        self.genres = Gtk.Box(spacing=4)
        [self.genres.pack_start(Gtk.Label(label=i, opacity=0.7), False, False, 0)
         for i in self.movie.getGenres()]

        print("ID:"+str(movie.getId()))
        self.grid = Gtk.Grid()
        self.grid.set_row_spacing(12)
        self.grid.attach(self.title, 0, 0, 2, 1)
        ratings_widget = getStarRating(ratings)
        ratings_widget.set_halign(Gtk.Align.END)
        ratings_widget.set_valign(Gtk.Align.CENTER)
        self.grid.attach(ratings_widget, 2, 0, 1, 1)
        self.grid.attach(self.genres, 0, 1, 3, 1)
        self.grid.attach(self.desc, 0, 2, 3, 1)

        self.divider.pack_end(self.grid, True, True, 0)
        self.add(self.divider)


class ListTile(Gtk.Box):
    def __init__(self, title, icon_name):
        Gtk.Box.__init__(self)
        icon = Gio.ThemedIcon(name=icon_name)
        image = Gtk.Image.new_from_gicon(icon, 6)
        label = Gtk.Label()
        label.set_markup(
            '<big><big><big><b>{}</b></big></big></big>'.format(title))
        self.pack_end(image, False, False, 6)
        self.pack_start(label, False, True, 6)


class MainStack(Gtk.Stack):
    def __init__(self, widgets):
        Gtk.Stack.__init__(self)
        self.set_transition_type(Gtk.StackTransitionType.SLIDE_UP_DOWN)
        self.set_transition_duration(700)
        for i, j in enumerate(widgets):
            self.add_titled(j, "widget"+str(i), "page"+str(i))


class LeftBar(Gtk.ScrolledWindow):
    def __init__(self, actions, left_bar_width=300, default_select=0):
        self.actions = actions
        Gtk.ScrolledWindow.__init__(self)
        self.set_min_content_width(left_bar_width)
        self.listview = Gtk.ListBox()
        # self.listview.set_selection_mode(0)
        self.listview.connect("row-activated", lambda x,
                              y: actions[abs(y.get_index())].go())
        for i, j in enumerate(self.actions):
            self.listview.insert(ListTile(j.title, j.icon_name), i)
        self.listview.select_row(
            self.listview.get_row_at_index(default_select))
        self.add(self.listview)
