from gi.repository import Gtk, Gio
import weather
LEFT_BAR_WIDTH = 300


class Action():
    def __init__(self, title, icon_name, function):
        self.function = function
        self.title = title
        self.icon_name = icon_name

    def go(self):
        self.function()


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


class WeatherBox(Gtk.Grid):
    def __init__(self):
        Gtk.Grid.__init__(self)
        curWeather = weather.Weather(testMode=False)
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
        label.set_markup(
            '<big><big><big><b>{}</b></big></big></big>'.format(str(curWeather.temperature)+"°C"))
        self.attach(label, 0, 1, 1, 1)


class LeftBar(Gtk.ScrolledWindow):
    def __init__(self):
        actions = [Action("Main", "go-home", lambda:0),
                   Action("Apps", "view-grid", lambda:0),
                   Action("Files", "folder", lambda:0),
                   Action("Settings", "open-menu", lambda:0), ]
        Gtk.ScrolledWindow.__init__(self)
        self.set_min_content_width(LEFT_BAR_WIDTH)
        self.listview = Gtk.ListBox()
        self.listview.set_selection_mode(0)
        self.listview.insert(WeatherBox(), 0)
        for i, j in enumerate(actions):
            self.listview.insert(ListTile(j.title, j.icon_name), i+1)
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
