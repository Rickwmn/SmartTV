from gi.repository import Gtk, Gdk, GdkPixbuf
import sqlite3
from requests import get
from os.path import isfile
from os import system
from utils import scaleImgToCard


class LoginButton(Gtk.Grid):
    def __init__(self, username, icon):
        self.username = username
        Gtk.Box.__init__(self)
        self.image = Gtk.Image()
        if not isfile("./cache/"+username+".jpg"):
            with open("./cache/"+username+".jpg", "wb") as file:
                file.write(get(icon).content)

        self.image = scaleImgToCard("./cache/"+username+".jpg", 128, 128)

        if len(username) > 18:
            username = username[:15]+"..."
        self.attach(self.image, 0, 0, 1, 1)
        self.label = Gtk.Label(label=username)
        self.label.set_line_wrap(True)
        self.label.set_justify(Gtk.Justification.CENTER)
        self.attach(self.label, 0, 1, 1, 1)

    def onClick(self):
        system("python ./gui.py "+self.username)


class MainWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="SmartTV OpenSource")
        self.set_default_size(Gdk.Screen.get_default().get_width(),
                              Gdk.Screen.get_default().get_height())

        self.flowbox = Gtk.FlowBox()
        self.flowbox.set_valign(Gtk.Align.CENTER)
        self.flowbox.set_halign(Gtk.Align.CENTER)
        self.flowbox.set_orientation(Gtk.Orientation.VERTICAL)
        self.flowbox.set_column_spacing(6)
        self.flowbox.set_selection_mode(Gtk.SelectionMode.NONE)
        self.add(self.flowbox)

        connection = sqlite3.connect("./settings/data.db")
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Data;")
        users = [LoginButton(i[1], i[8]) for i in cursor.fetchall()]
        for i in users:
            self.flowbox.add(i)
        self.flowbox.connect("child_activated", lambda _,
                             x: users[x.get_index()].onClick())
        self.flowbox.unselect_all()


window = MainWindow()
window.fullscreen()
window.connect("destroy", Gtk.main_quit)
window.show_all()
Gtk.main()
