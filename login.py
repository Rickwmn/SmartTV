from gi.repository import Gtk,  GdkPixbuf
import sqlite3
from requests import get
from os.path import isfile
from os import system
from utils import getCardImg
import multiprocessing
from screeninfo import get_monitors

if not isfile("./settings/data.db"):
    system("python3 setup.py")


class LoginButton(Gtk.Button):
    def __init__(self, username, icon):
        self.username = username
        Gtk.Bin.__init__(self)
        self.image = getCardImg(
            icon, "./cache/"+"username="+username+".jpg", 128, 128)

        if len(username) > 18:
            username = username[:15]+"..."
        self.grid = Gtk.Grid()
        self.grid.attach(self.image, 0, 0, 1, 1)
        self.label = Gtk.Label(label=username)
        self.label.set_justify(Gtk.Justification.CENTER)
        self.grid.attach(self.label, 0, 1, 1, 1)
        self.add(self.grid)

    def onClick(self, x):
        system("python ./gui.py "+self.username)
        Gtk.main_quit()


class MainWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="SmartTV OpenSource")
        self.set_default_size(get_monitors()[0].width,get_monitors()[0].height)
        self.grid = Gtk.Grid()
        self.grid.set_valign(Gtk.Align.CENTER)
        self.grid.set_halign(Gtk.Align.CENTER)
        self.grid.set_orientation(Gtk.Orientation.VERTICAL)
        self.grid.set_column_spacing(6)
        self.grid.set_row_spacing(6)
        self.add(self.grid)

        connection = sqlite3.connect("./settings/data.db")
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Data;")
        users = [LoginButton(i[1], i[9]) for i in cursor.fetchall()]
        for i, j in enumerate(users):
            j.connect("clicked", j.onClick)
            self.grid.attach(j, i % 7, i//7, 1, 1)


window = MainWindow()
window.fullscreen()
window.connect("destroy", Gtk.main_quit)
window.show_all()
Gtk.main()
