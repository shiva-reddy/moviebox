from gi.repository import Gtk
#
class MyWindow(Gtk.Window):

    def __init__(self):

        Gtk.Window.__init__(self, title="Hello World")
        self.set_border_width(10)
        self.box = Gtk.Box(spacing=6)
        self.add(self.box)
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)

        self.entry = Gtk.Entry()
        self.box.pack_start(self.entry, True, True, 0)

        self.button = Gtk.Button(label="Search")
        self.button.connect("clicked", self.on_button_clicked)
        self.box.pack_start(self.button, True, True, 0)
        
        filter_store = Gtk.ListStore(int, str)
        filter_store.append([1, "Title"])
        filter_store.append([2, "Directors"])
        filter_store.append([3, "Genre"])
        filter_store.append([4, "Actors"])
        filter_combo = Gtk.ComboBox.new_with_model(filter_store)
        filter_combo.connect("changed", self.on_filter_combo_changed)
        renderer_text = Gtk.CellRendererText()
        filter_combo.add_attribute(renderer_text, "text", 0)
        vbox.pack_start(filter_combo, False, False, True)
        filter_combo.pack_start(renderer_text, True)

    def on_button_clicked(self, widget):
        print("Hello")

    def on_button2_clicked(self, widget):
        print("Goodbye")

    def on_filter_combo_changed(self, combo):
        print("Filter Changed")

win = MyWindow()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()