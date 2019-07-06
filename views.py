from gi.repository import Gtk, Gio, Gdk
from utils import getCardImg


class MoviePreview(Gtk.Window):
    def __init__(self, movie):
        Gtk.Window.__init__(self, title="SmartTV OpenSource")
        self.set_default_size(Gdk.Screen.get_default().get_width(),
                              Gdk.Screen.get_default().get_height())
        self.movie = movie
        self.divider = Gtk.Grid()
        self.divider.set_hexpand(True)
        self.divider.set_vexpand(True)
        self.divider.attach(getCardImg(
            movie.getCovers()[2], "./cache/cover-large={}".format(movie.getTitle())+".png", width=500, heigth=750), 0, 0, 1, 1)
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
