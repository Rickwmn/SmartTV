from gi.repository import Gtk, Gio, Gdk, GdkPixbuf
from views import LeftBar
from utils import Action
from sys import argv

# class MainView:
LEFT_BAR_WIDTH = int(argv[1])


class SettingsStack(Gtk.Stack):
    def __init__(self, widgets):
        Gtk.Stack.__init__(self)
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
            Action("General", "bla", lambda:switchStack(0, self.settings_view)),
            Action("Look", "bla", lambda:switchStack(1, self.settings_view)),
            Action("Torrent", "torrent", lambda:switchStack(
                2, self.settings_view))
        ]

        self.main_divider = Gtk.Box(spacing=6)
        self.add(self.main_divider)
        self.leftbar = LeftBar(
            actions=left_bar_actions, left_bar_width=LEFT_BAR_WIDTH, start_index=0)
        self.main_divider.pack_start(self.leftbar, False, True, 0)
        self.settings_view = SettingsStack(
            [Gtk.Label(label="General"), Gtk.Label(label="Look"), Gtk.Label(label="Torrent")])
        self.main_divider.pack_end(self.settings_view, True, True, 0)


window = Settings()
window.fullscreen()
window.connect("destroy", Gtk.main_quit)
window.show_all()
Gtk.main()
