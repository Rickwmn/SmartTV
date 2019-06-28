from gi.repository import Gtk, Gio, Gdk, GdkPixbuf
from views import LeftBar
from utils import Action
from sys import argv
import sqlite3


connection = sqlite3.connect("./settings/data.db")
cursor = connection.cursor()
cursor.execute("SELECT * FROM Data WHERE username=\"{}\"".format(argv[1]))
settings = cursor.fetchone()

LEFT_BAR_WIDTH = settings[9]


def propLabel(text):
    label = Gtk.Label()
    label.set_markup("<big>{}</big>".format(text))
    return label


def generalSettings():
    grid = Gtk.Grid()
    grid.set_row_spacing(18)

    end = 3
    title = Gtk.Label()
    title.set_markup(
        "<big><big><big><big><big>General Settings</big></big></big></big></big>")
    title.set_hexpand(True)
    grid.attach(title, 0, 0, end, 1)

    grid.attach(propLabel("Username"), 0, 1, 1, 1)
    grid.attach(propLabel("E-Mail"), 0, 2, 1, 1)
    grid.attach(propLabel("Units"), 0, 3, 1, 1)
    grid.attach(propLabel("Location"), 0, 4, 1, 1)
    grid.attach(propLabel("Timezone"), 0, 5, 1, 1)
    spacer = Gtk.Label()
    spacer.set_hexpand(True)
    grid.attach(spacer, 1, 1, 1, 1)
    return grid


class SettingsStack(Gtk.Stack):
    def __init__(self, widgets):
        Gtk.Stack.__init__(self)
        self.set_transition_type(Gtk.StackTransitionType.SLIDE_UP_DOWN)
        self.set_transition_duration(700)
        for i, j in enumerate(widgets):
            self.add_titled(j, "widget"+str(i), "page"+str(i))


def switchStack(index, stack):
    stack.set_visible_child(stack.get_children()[index])
    stack.get_children()[index].show()


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
            actions=left_bar_actions, left_bar_width=LEFT_BAR_WIDTH, start_index=0)
        self.main_divider.pack_start(self.leftbar, False, True, 0)
        self.settings_view = SettingsStack(
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
