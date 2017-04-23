import urllib2
from bs4 import BeautifulSoup
import sqlite3
from ConfigParser import SafeConfigParser

conn = sqlite3.connect('play.db')
cursor = conn.cursor()

parser = SafeConfigParser()
parser.read('config_crawler.ini')

level = 2
baseURL = "https://play.google.com"
relat = "/store/apps/details?id=com.playappking.busrush&hl=en"

#cursor.execute('''CREATE TABLE crawl (ID int auto_increment, url text )''')
#cursor.execute('''CREATE TABLE crawl (num INTEGER PRIMARY KEY AUTOINCREMENT, url text )''')
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
					cursor.execute("INSERT INTO crawl (url) VALUES (?);", ( str ( link [ child3 ] ), ) )
				conn.commit()
				crawl(link[child3],max-1)
	except:
		print "dodged exception !"


def main():
	seed = dict( parser.items('seeds') )
	# print seed
	for key, value in seed.iteritems():
		# print value
		crawl(str(value),level)
	# crawl(s,level)

if __name__== "__main__":
  main()
