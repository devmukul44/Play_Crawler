import urllib2
from bs4 import BeautifulSoup
import sqlite3
from ConfigParser import SafeConfigParser

parser = SafeConfigParser()
parser.read('config.ini')
print parser.get('bug_tracker', 'url')

conn = sqlite3.connect('example.db')

cursor = conn.cursor()

# cursor.execute('''CREATE TABLE stocks
#              (date text, trans text, symbol text, qty real, price real)''')

cursor.execute("INSERT INTO stocks VALUES ('2006-01-05','BUY','RHAT',100,35.14)")

cursor.execute("select * from stocks")
print cursor.fetchone()

cursor = conn.execute("SELECT * from stocks")
for row in cursor:
   print row[0] , row[1] , row[2] , row[3]

conn.commit()
conn.close()