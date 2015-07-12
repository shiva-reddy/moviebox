#The purpose of this script is to return a row based on the element being searched for.
import os
import sys
import sqlite3
from subprocess import call

def search(type,element):
	conn=sqlite3.connect('lm.db')
	c=conn.cursor()
	element='%'+element+'%'
	sql="SELECT * FROM imtab WHERE %s like \'%s\'" %(type,element)
#	print sql
	for row in c.execute(sql):
		print row



search(str(sys.argv[1]),str(sys.argv[2]))