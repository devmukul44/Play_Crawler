import sqlite3
import csv

conn = sqlite3.connect('play.db')
cursor = conn.cursor()
cur = conn.execute("SELECT * from crawl;")

result=cur.fetchall()
c = csv.writer(open("temp.csv","wb"))

for row in result:
    c.writerow(row)
