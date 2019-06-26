from gi.repository import Gtk, Gio


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


class LeftBar(Gtk.ScrolledWindow):
    def __init__(self, actions, left_bar_width=300, start_index=0):
        self.actions = actions
        Gtk.ScrolledWindow.__init__(self)
        self.set_min_content_width(left_bar_width)
        self.listview = Gtk.ListBox()
        self.listview.set_selection_mode(0)
        self.listview.connect("row-activated", lambda x,
                              y: actions[abs(y.get_index()-1)].go())
        for i, j in enumerate(self.actions):
            self.listview.insert(ListTile(j.title, j.icon_name), i+start_index)
        self.add(self.listview)
