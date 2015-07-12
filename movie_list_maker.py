import sys
import os
import sqlite3
from subprocess import call

def main():
	rootDir=str(sys.argv[1])
	conn=sqlite3.connect('lm.db')
	c=conn.cursor()
	for dirName, subdirList, fileList in os.walk(rootDir):
		for fname in fileList:
			fileExtension=fname[-3:]
			if fileExtension == "mkv" or fileExtension == "avi" or fileExtension == "mp4":
				if not "'" in fname:
					#print dirName
					sql="INSERT INTO %s VALUES ('%s','%s')" %("path_filename_list",dirName,fname)
					#print sql
					c.execute(sql)
	conn.commit()
	conn.close()
if __name__ == "__main__":
    main()