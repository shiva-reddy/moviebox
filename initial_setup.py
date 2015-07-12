#This script runs only the first time and creates a database

import os
import sys
import sqlite3
from subprocess import call
call(["touch","lm.db"])
conn=sqlite3.connect('lm.db')
c=conn.cursor()
c.execute('''create table imtab (id text,name text,year number,director text,actors text,genre text,metasc real,imdbrat real)''')
c.execute('''create table path_filename_list (path text,filename text)''')
c.execute('''create table path_name (filename text,name text)''')