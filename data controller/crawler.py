import urllib2
from bs4 import BeautifulSoup
import mysql.connector
from mysql.connector import Error
from ConfigParser import SafeConfigParser

try:
	conn = mysql.connector.connect(host='localhost', database='play', user='root', password='root')
	cursor = conn.cursor()
	cursor.execute("CREATE TABLE crawl ( id int(10) auto_increment primary key, url varchar(1000) )")
except Error as e:
	print(e)

parser = SafeConfigParser()
parser.read('config_crawler.ini')

level = 2
baseURL = "https://play.google.com"
relat = "/store/apps/details?id=com.playappking.busrush&hl=en"

def crawl(relativeURL,max) :
	try:
		if(max > 0):
			url = baseURL + relativeURL
			response = urllib2.urlopen(url).read()

			soup = BeautifulSoup(response, 'html.parser')

			parent = parser.get('crawler_config','parent_tag')
			child1 = parser.get('crawler_config','child_1_tag')
			child2 = parser.get('crawler_config','child_2_tag')
			child3 = parser.get('crawler_config','child_3_tag')

			# for link in soup.find_all('a', attrs = {'class' : 'title'}):
			for link in soup.find_all(parent , attrs = {child1 : child2}):
				print str( link[ child3 ] )
				if( int( str( link[child3] ).find("info/topic")) + 1 ):
					print("dodged an error")
				else:
					add_entry = ("INSERT INTO crawl "
					"(url) "
					"VALUES ( %(url)s); ")
					args = {
					'url': str( link[ child3 ] ),
					}
					cursor.execute(add_entry, args)
					conn.commit()
				crawl(link[child3],max-1)
	except Error as e:
		print(e)


def main():
	seed = dict( parser.items('seeds') )
	# print seed
	for key, value in seed.iteritems():
		# print value
		crawl(str(value),level)
	# crawl(s,level)
	conn.close()

if __name__== "__main__":
  main()
