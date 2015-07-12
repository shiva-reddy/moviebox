from gi.repository import Gtk, Pango
import sqlite3
import os


class SearchDialog(Gtk.Dialog):

    def __init__(self, parent):
        Gtk.Dialog.__init__(self, "Search", parent,
            Gtk.DialogFlags.MODAL, buttons=(
            Gtk.STOCK_FIND, Gtk.ResponseType.OK,
            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL))

        box = self.get_content_area()

        label = Gtk.Label("Insert text you want to search for:")
        box.add(label)

        self.entry = Gtk.Entry()
        box.add(self.entry)

        self.show_all()

class TextViewWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title='Movie')
        #self.connect('delete-event', Gtk.main_quit)        
        
        

        self.set_default_size(800,600)

        self.grid = Gtk.Grid()
        self.add(self.grid)

        self.create_textview()
        self.create_toolbar()
        #self.create_buttons()


	 


    # Add data to ListStore
    def populate_store(self, store):
            conn=sqlite3.connect('lm.db')
            c=conn.cursor()
            sql="SELECT * FROM imtab"
            for row in c.execute(sql):
                imdb_id=row[0]
                name=row[1]
                Directors=row[3]
                Genre=row[5]
                Cast=row[4]
                store.append([name,Directors,Cast,Genre])


    def create_toolbar(self):
        toolbar = Gtk.Toolbar()
        self.grid.attach(toolbar, 0, 0, 3, 1)

        button_search = Gtk.ToolButton.new_from_stock(Gtk.STOCK_FIND)
        button_search.connect("clicked", self.on_search_clicked)
        toolbar.insert(button_search, 0)

    def create_textview(self):
        # scrolledwindow = Gtk.ScrolledWindow()
        # scrolledwindow.set_hexpand(True)
        # scrolledwindow.set_vexpand(True)
        # self.grid.attach(scrolledwindow, 0, 1, 3, 1)

        # self.textview = Gtk.TextView()
        # self.textbuffer = self.textview.get_buffer()
        # self.textbuffer.set_text("This is some text inside of a Gtk.TextView. "
        #     + "Select text and click one of the buttons 'bold', 'italic', "
        #     + "or 'underline' to modify the text accordingly.")
        # scrolledwindow.add(self.textview)

        # self.tag_bold = self.textbuffer.create_tag("bold",
        #     weight=Pango.Weight.BOLD)
        # self.tag_italic = self.textbuffer.create_tag("italic",
        #     style=Pango.Style.ITALIC)
        # self.tag_underline = self.textbuffer.create_tag("underline",
        #     underline=Pango.Underline.SINGLE)
        # self.tag_found = self.textbuffer.create_tag("found",
        #     background="yellow")
        Gtk.Window.__init__(self, title='My Window Title')
        self.connect('delete-event', Gtk.main_quit)        
        
        store = Gtk.ListStore(str, str, str, str)
        self.populate_store(store)
        
        self.treeview = Gtk.TreeView(model=store)

        renderer = Gtk.CellRendererText()
        
        column_catalog = Gtk.TreeViewColumn('Title', renderer, text=0)
        column_catalog.set_sort_column_id(0)        
        self.treeview.append_column(column_catalog)
        
        column_dbname = Gtk.TreeViewColumn('Directors', renderer, text=1)
        column_dbname.set_sort_column_id(1)
        self.treeview.append_column(column_dbname)
        
        column_charset = Gtk.TreeViewColumn('Cast', renderer, text=2)
        column_charset.set_sort_column_id(2)
        self.treeview.append_column(column_charset)
        
        column_collation = Gtk.TreeViewColumn('Genre', renderer, text=3)
        column_collation.set_sort_column_id(3)
        self.treeview.append_column(column_collation)
        
        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.set_policy(
            Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scrolled_window.add(self.treeview)

    def create_buttons(self):
        check_editable = Gtk.CheckButton("Editable")
        check_editable.set_active(True)
        check_editable.connect("toggled", self.on_editable_toggled)
        self.grid.attach(check_editable, 0, 2, 1, 1)

        check_cursor = Gtk.CheckButton("Cursor Visible")
        check_cursor.set_active(True)
        check_editable.connect("toggled", self.on_cursor_toggled)
        self.grid.attach_next_to(check_cursor, check_editable,
            Gtk.PositionType.RIGHT, 1, 1)

        radio_wrapnone = Gtk.RadioButton.new_with_label_from_widget(None,
            "No Wrapping")
        self.grid.attach(radio_wrapnone, 0, 3, 1, 1)

        radio_wrapchar = Gtk.RadioButton.new_with_label_from_widget(
            radio_wrapnone, "Character Wrapping")
        self.grid.attach_next_to(radio_wrapchar, radio_wrapnone,
            Gtk.PositionType.RIGHT, 1, 1)

        radio_wrapword = Gtk.RadioButton.new_with_label_from_widget(
            radio_wrapnone, "Word Wrapping")
        self.grid.attach_next_to(radio_wrapword, radio_wrapchar,
            Gtk.PositionType.RIGHT, 1, 1)

        radio_wrapnone.connect("toggled", self.on_wrap_toggled,
            Gtk.WrapMode.NONE)
        radio_wrapchar.connect("toggled", self.on_wrap_toggled,
            Gtk.WrapMode.CHAR)
        radio_wrapword.connect("toggled", self.on_wrap_toggled,
            Gtk.WrapMode.WORD)

    def on_button_clicked(self, widget, tag):
        bounds = self.textbuffer.get_selection_bounds()
        if len(bounds) != 0:
            start, end = bounds
            self.textbuffer.apply_tag(tag, start, end)

    def on_clear_clicked(self, widget):
        start = self.textbuffer.get_start_iter()
        end = self.textbuffer.get_end_iter()
        self.textbuffer.remove_all_tags(start, end)

    def on_editable_toggled(self, widget):
        self.textview.set_editable(widget.get_active())

    def on_cursor_toggled(self, widget):
        self.textview.set_cursor_visible(widget.get_active())

    def on_wrap_toggled(self, widget, mode):
        self.textview.set_wrap_mode(mode)

    def on_justify_toggled(self, widget, justification):
        self.textview.set_justification(justification)

    def on_search_clicked(self, widget):
        dialog = SearchDialog(self)
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            cursor_mark = self.textbuffer.get_insert()
            start = self.textbuffer.get_iter_at_mark(cursor_mark)
            if start.get_offset() == self.textbuffer.get_char_count():
                start = self.textbuffer.get_start_iter()

            self.search_and_mark(dialog.entry.get_text(), start)

        dialog.destroy()

    def search_and_mark(self, text, start):
        end = self.textbuffer.get_end_iter()
        match = start.forward_search(text, 0, end)

        if match != None:
            match_start, match_end = match
            self.textbuffer.apply_tag(self.tag_found, match_start, match_end)
            self.search_and_mark(text, match_end)

win = TextViewWindow()
win.connect("delete-event", Gtk.main_quit)
win.show_all()

Gtk.main()
