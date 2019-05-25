from gi.repository import Gtk, Gio


class Action():
    def __init__(self, title, icon_name, function):
        self.function = function
        self.title = title
        self.icon_name = icon_name

    def go(self):
        self.function()


class ListTile(Gtk.Box):
<<<<<<< HEAD
    def __init__(self, title, icon_name):
=======
    def __init__(self, icon_name, title):
>>>>>>> 060e5289b33532f320ff21ed75a06e33894e2be4
        Gtk.Box.__init__(self)
        icon = Gio.ThemedIcon(name=icon_name)
        image = Gtk.Image.new_from_gicon(icon, 6)
        label = Gtk.Label()
        label.set_markup(
<<<<<<< HEAD
            '<big><big><big><b>{}</b></big></big></big>'.format(title))
=======
            '<big><b><big>{}</big></b></big>'.format(title))
>>>>>>> 060e5289b33532f320ff21ed75a06e33894e2be4
        self.pack_end(image, False, False, 6)
        self.pack_start(label, False, True, 6)


class LeftBar(Gtk.ScrolledWindow):
    def __init__(self):
<<<<<<< HEAD
        actions = [Action("Main", "go-home", lambda:0),
                   Action("Apps", "open-menu", lambda:0),
                   Action("Files", "folder", lambda:0),
                   Action("Settings", "open-menu", lambda:0), ]
=======
>>>>>>> 060e5289b33532f320ff21ed75a06e33894e2be4
        Gtk.ScrolledWindow.__init__(self)
        self.set_min_content_width(300)
        self.listview = Gtk.ListBox()
        self.listview.set_selection_mode(0)
<<<<<<< HEAD
        for i, j in enumerate(actions):
            self.listview.insert(ListTile(j.title, j.icon_name), i)
=======
        for i, j in enumerate(["open-menu"]):
            self.listview.insert(ListTile(j, j), i)
>>>>>>> 060e5289b33532f320ff21ed75a06e33894e2be4
        self.add(self.listview)


class MainWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="SmartTV OpenSource")
        self.main_divider = Gtk.Box(spacing=6)
        self.add(self.main_divider)
        self.main_divider.pack_start(LeftBar(), False, True, 0)
        self.main_divider.pack_end(Gtk.Box(), True, True, 0)


window = MainWindow()
window.fullscreen()
window.connect("destroy", Gtk.main_quit)
window.show_all()
Gtk.main()
