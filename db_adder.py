#This script takes a movie name as input and adds metadata to the file lm.db

import requests
import os
import sys
import urllib
import unicodedata
import codecs
import sqlite3
from bs4 import BeautifulSoup
from subprocess import call


def main():
	no_of_words=len(sys.argv)
	url="http://www.omdbapi.com/?t="
	user_input=str(sys.argv[1])

	i=2
	while (i<no_of_words):
		user_input+="+"
		user_input+=str(sys.argv[i])
		i+=1
#---------------------------------------------------------omdb api parameters
	type_val="movie"
	y_val="no"
	r_val="xml"
	t_val=user_input
	tomatoes_val="true"
	plot_val="full"
	s_val=user_input
	net_url=url+user_input+"&plot="+plot_val+"&r="+r_val
	parse(net_url)
#----------------------------------------------------------data parsing

def parse(net_url):
	r=requests.get(net_url)
	soup=BeautifulSoup(r.content)
	response=soup.root.get("response").encode()
	print response
	if response == "False":
		print "Sorry..could not find your movie:-"+user_input
		sys.exit(0)
	title=soup.movie.get("title")
	year=soup.movie.get("year")
	genre=soup.movie.get("genre")
	director=soup.movie.get("director")
	actors=soup.movie.get("actors")
	poster_url=soup.movie.get("poster")
	metascore=soup.movie.get("metascore")
	imdbRating=soup.movie.get("imdbrating")
	imdbID=soup.movie.get("imdbid")
	plot=soup.movie.get("plot")

#----------------------------------------------------------creating poster and plot files
	verify(title)
	call(["mkdir","."+title])
	file_name="."+title+"/"+title+"_plot.txt"
	image_name="."+title+"/"+title+"_img.jpg"
	call(["touch",image_name])
	urllib.urlretrieve(poster_url,image_name)
	call(["touch",file_name])
	output=open(file_name,'w')
	output.write(plot)
	output.close()

#----------------------------------------------------------adding to database
	conn=sqlite3.connect('lm.db')
	c=conn.cursor()
	sql="INSERT INTO imtab VALUES ('%s','%s','%s','%s','%s','%s','%s','%s')" %(imdbID,title,year,director,actors,genre,metascore,imdbRating)
	c.execute(sql)
	conn.commit()
	conn.close()

def verify(title):
	conn=sqlite3.connect('lm.db')
	c=conn.cursor()
	counter=0
	sql="SELECT name FROM imtab WHERE name like \'%s\'" %(title)
	for row in c.execute(sql):
		counter=counter+1
	conn.close()
	if counter!=0:
		sys.exit()
if __name__ == "__main__":
    main()
