import os, sqlite3

conn = sqlite3.connect('lm.db')
conn.text_factory = str ## my current (failed) attempt to resolve this
cur = conn.cursor()
data = cur.execute("SELECT * FROM imtab")

f = open('output.csv', 'w')
print >> f, "Column1, Column2, Column3, Etc."
for row in data:
  print >> f, row
f.close()