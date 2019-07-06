from gi.repository import Gtk, Gio, Gdk, GdkPixbuf
from views import LeftBar, MainStack
from utils import Action, switchStack
from sys import argv
import sqlite3


connection = sqlite3.connect("./settings/data.db")
cursor = connection.cursor()
cursor.execute("SELECT * FROM Data WHERE username=\"{}\"".format(argv[1]))
settings = cursor.fetchone()

LEFT_BAR_WIDTH = settings[10]


def propLabel(text):
    label = Gtk.Label()
    label.set_markup("<big>{}</big>".format(text))
    return label


class Properties(Gtk.Grid):
    def __init__(self, main_title, titles, _settings, widgets):
        Gtk.Window.__init__(self)
        self.set_row_spacing(18)
        title = Gtk.Label()
        title.set_markup(
            "<big><big><big><big><big>{}</big></big></big></big></big>".format(main_title))
        title.set_hexpand(True)
        self.attach(title, 0, 0, 3, 1)

        for i in range(len(_settings)):
            temp_label = Gtk.Label()
            temp_label.set_markup("<big>{}</big>".format(titles[i]))
            self.attach(temp_label, 0, i+1, 1, 1)
            spacer = Gtk.Label()
            spacer.set_hexpand(True)
            self.attach(spacer, 1, i+1, 1, 1)
            if type(widgets[i]) == type(Gtk.Label()):
                widgets[i].set_label(settings[_settings[i]])
            elif type(widgets[i]) == type(Gtk.Entry()):
                widgets[i].set_text(settings[_settings[i]])
            self.attach(widgets[i], 2, i+1, 1, 1)
        self.attach(Gtk.Button(label="Apply"), 2, len(settings), 1, 1)


def generalSettings():

    titles = ["Username", "E-Mail", "Units",
              "Country", "Region", "City", "Timezone"]
    _settings = [1, 2, 4, 5, 6, 7, 8]
    widgets = [Gtk.Entry(), Gtk.Entry(), Gtk.ComboBox(),
               Gtk.Label(), Gtk.Label(), Gtk.Label(), Gtk.Label()]
    return Properties("General Settings", titles, _settings, widgets)


class Settings(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="SmartTV OpenSource")
        self.set_default_size(Gdk.Screen.get_default().get_width(),
                              Gdk.Screen.get_default().get_height())
        left_bar_actions = [
            Action("Back", "go-previous", lambda:Gtk.main_quit()),
            Action("General", "preferences-desktop",
                   lambda:switchStack(0, self.settings_view)),
            Action("Look", "preferences-desktop-theme",
                   lambda:switchStack(1, self.settings_view)),
            Action("Torrent", "torrent", lambda:switchStack(
                2, self.settings_view)),
            Action("Other", "preferences-other", lambda:switchStack(
                3, self.settings_view))
        ]

        self.main_divider = Gtk.Box(spacing=6)
        self.add(self.main_divider)
        self.leftbar = LeftBar(
            actions=left_bar_actions, left_bar_width=LEFT_BAR_WIDTH, default_select=1)
        self.main_divider.pack_start(self.leftbar, False, True, 0)
        self.settings_view = MainStack(
            [
                generalSettings(),
                Gtk.Label(label="Look"),
                Gtk.Label(label="Torrent"),
                Gtk.Label(label="Other")
            ])
        self.main_divider.pack_end(self.settings_view, True, True, 0)


window = Settings()
window.fullscreen()
window.connect("destroy", Gtk.main_quit)
window.show_all()
Gtk.main()
