import urllib2
from bs4 import BeautifulSoup
import mysql.connector
from mysql.connector import Error
from ConfigParser import SafeConfigParser
import csv

try:
    conn = mysql.connector.connect(host='localhost', database='play', user='root', password='root')
    cursor = conn.cursor(buffered = True)
    cursor.execute("CREATE TABLE scrap ( id int(10) auto_increment primary key, name varchar(1000), genre varchar(100), developer varchar(1000), downloads varchar(100), updatedOn varchar(100), contentRating varchar(100), score varchar(100))")
except Error as e:
    print(e)

parser = SafeConfigParser()
parser.read('config_scraper.ini')

baseURL = "https://play.google.com"
relat = "/store/apps/details?id=com.playappking.busrush&hl=en"

# response = urllib2.urlopen(url)
# html = response.read()

# soup = BeautifulSoup(html, 'html.parser')
# # readable = soup.prettify()
# file_name = str(soup.title).split('>')[1].split('<')[0] + ".html"
#print file_name
# t = soup.title.string
# print t
#file_name = url.split('/')[-1] + ".html"
# with open(file_name, 'wb') as f:
#     f.write(str(soup))

with open('scrap.csv', 'a') as csvfile:
  fieldnames = ['name' , 'genre', 'developer', 'downloads', 'updatedOn', 'contentRating', 'score', 'scoreClass']
  writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
  writer.writeheader()

def scrap(relativeURL):
    try:
      url = baseURL + relativeURL
      response = urllib2.urlopen(url)
      html = response.read()
      soup = BeautifulSoup(html, 'html.parser')

      parent_name = parser.get('scraper_config_name','parent_tag')
      child1_name = parser.get('scraper_config_name','child_1_tag')
      child2_name = parser.get('scraper_config_name','child_2_tag')

      parent_data = parser.get('scraper_config_data','parent_tag')
      child1_data = parser.get('scraper_config_data','child_1_tag')
      child2_data = parser.get('scraper_config_data','child_2_tag')

      parent_genre = parser.get('scraper_config_genre','parent_tag')
      child1_genre = parser.get('scraper_config_genre','child_1_tag')
      child2_genre = parser.get('scraper_config_genre','child_2_tag')

      parent_developer = parser.get('scraper_config_developer','parent_tag')
      child1_developer = parser.get('scraper_config_developer','child_1_tag')
      child2_developer = parser.get('scraper_config_developer','child_2_tag')

      parent_downloads = parser.get('scraper_config_downloads','parent_tag')
      child1_downloads = parser.get('scraper_config_downloads','child_1_tag')
      child2_downloads = parser.get('scraper_config_downloads','child_2_tag')

      parent_updatedOn = parser.get('scraper_config_updatedOn','parent_tag')
      child1_updatedOn = parser.get('scraper_config_updatedOn','child_1_tag')
      child2_updatedOn = parser.get('scraper_config_updatedOn','child_2_tag')

      parent_score = parser.get('scraper_config_score','parent_tag')
      child1_score = parser.get('scraper_config_score','child_1_tag')
      child2_score = parser.get('scraper_config_score','child_2_tag')


      title_name = soup.find(parent_name, attrs = {child1_name : child2_name}).text.strip()
      print title_name
    #   data = soup.find(parent_data, attrs = {child1_data : child2_data}).text.strip()
      genre =  soup.find(parent_genre, attrs = {child1_genre : child2_genre}).text.strip()
      developer = soup.find(parent_developer, attrs = {child1_developer : child2_developer}).text.strip()
      downloads = soup.find(parent_downloads, attrs = {child1_downloads : child2_downloads}).text.strip()
      updatedOn = soup.find(parent_updatedOn, attrs = {child1_updatedOn : child2_updatedOn}).text.strip()
      score =  float(soup.find(parent_score, attrs = {child1_score : child2_score}).text.strip())
      contentRating =  soup.find('div', attrs = {'itemprop' : 'contentRating'}).text.strip()

      scoreClass = "1 (0.1 - 1.0)"
      if(score < 1.1):
          scoreClass = "1 (0.1 - 1.0)"
      elif(score > 1.0 and score < 2.1):
          scoreClass = "2 (1.1 - 2.0)"
      elif(score > 2.0 and score < 3.1):
          scoreClass = "3 (2.1 - 3.0)"
      elif(score > 3.0 and score < 4.1):
          scoreClass = "4 (3.1 - 4.0)"
      elif(score > 4.0 and score <= 5.0):
          scoreClass = "5 (4.1 - 5.0)"

      add_entry = ("INSERT INTO scrap "
      "(name , genre, developer, downloads, updatedOn, contentRating, score) "
      "VALUES ( %(name)s, %(genre)s, %(developer)s, %(downloads)s, %(updatedOn)s, %(contentRating)s, %(score)s ); ")
      args = {
      'name': title_name,
      'genre': genre,
      'developer': developer,
      'downloads': downloads,
      'updatedOn': updatedOn,
      'contentRating': contentRating,
      'score': score,
      }
      cursor.execute(add_entry, args)
      conn.commit()
      with open('scrap.csv', 'a') as csvfile:
          fieldnames = ['name' , 'genre', 'developer', 'downloads', 'updatedOn', 'contentRating', 'score', 'scoreClass']
          writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
          writer.writerow({'name' : title_name , 'genre' : genre , 'developer' : developer , 'downloads' : downloads , 'updatedOn' : updatedOn , 'contentRating' : contentRating, 'score' : score, 'scoreClass' : scoreClass })
    except Error as e:
        print e
    except:
        print "dodged exception !"
def main():
    cursor = conn.cursor(buffered = True)
    query = ("SELECT DISTINCT url FROM crawl;")
    cursor.execute(query)
    for row in cursor:
        scrap(row[0])

if __name__== "__main__":
  main()
