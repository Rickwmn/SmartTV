from gi.repository import Gtk, Gio, Gdk, GdkPixbuf
from views import LeftBar


class Settings(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="SmartTV OpenSource")
        self.set_default_size(Gdk.Screen.get_default().get_width(),
                              Gdk.Screen.get_default().get_height())
    left_bar_actions = [

    ]


window = Settings()
window.fullscreen()
window.connect("destroy", Gtk.main_quit)
window.show_all()
Gtk.main()
