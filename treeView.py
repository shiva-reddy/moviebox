#! /usr/bin/python


from gi.repository import Gtk
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



class MyWindow(Gtk.Window):
    
    def __init__(self):

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
        scrolled_window.set_min_content_height(200)

        self.add(scrolled_window)
        self.show_all()
		
	   
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


win = MyWindow()
Gtk.main()
