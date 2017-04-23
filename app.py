from flask import Flask
from flask import render_template
import mysql.connector
from mysql.connector import Error
import csv


try:
    conn = mysql.connector.connect(host='localhost', database='play', user='root', password='root')
    cursor = conn.cursor(buffered = True)
except Error as e:
    print(e)

app = Flask(__name__)

def get_csv():
    csv_path = './static/play-scrap-csv/part-00000'
    csv_file = open(csv_path, 'rb')
    csv_obj = csv.DictReader(csv_file)
    csv_list = list(csv_obj)
    return csv_list

def get_db():
    cursor = conn.cursor()
    query = ("SELECT count(*) FROM scrap_copy;")
    cursor.execute(query)
    row = str(cursor.fetchone()).split("(")[1].split(",")[0]
    # dblist = [collected, crawled, parsed]
    return row

def get_csv_genre():
    csv_path = './static/genre-csv/part-00000'
    csv_file = open(csv_path, 'rb')
    csv_obj = csv.DictReader(csv_file)
    csv_list = list(csv_obj)
    return csv_list

def get_csv_downloads():
    csv_path = './static/downloads-csv/part-00000'
    csv_file = open(csv_path, 'rb')
    csv_obj = csv.DictReader(csv_file)
    csv_list = list(csv_obj)
    return csv_list

def get_csv_contents():
    csv_path = './static/content-rate-csv/part-00000'
    csv_file = open(csv_path, 'rb')
    csv_obj = csv.DictReader(csv_file)
    csv_list = list(csv_obj)
    return csv_list

def get_csv_ratings():
    csv_path = './static/score-class-csv/part-00000'
    csv_file = open(csv_path, 'rb')
    csv_obj = csv.DictReader(csv_file)
    csv_list = list(csv_obj)
    return csv_list

def get_csv_instances():
    csv_path = './boto3/aws_instance.csv'
    csv_file = open(csv_path, 'rb')
    csv_obj = csv.DictReader(csv_file)
    csv_list = list(csv_obj)
    return csv_list


@app.route("/")
def index():
    template = 'index.html'
    object_list = get_csv()
    dblist = get_db()
    return render_template(template, object_list=object_list, dblist = dblist)

@app.route("/genre/")
def genre():
    template = 'genre.html'
    object_list = get_csv_genre()
    return render_template(template, object_list=object_list)

@app.route("/downloads/")
def downloads():
    template = 'downloads.html'
    object_list = get_csv_downloads()
    return render_template(template, object_list=object_list)

@app.route("/content_rate/")
def content_rate():
    template = 'content_rate.html'
    object_list = get_csv_contents()
    return render_template(template, object_list=object_list)

@app.route("/rating/")
def rating():
    template = 'rating.html'
    object_list = get_csv_ratings()
    return render_template(template, object_list=object_list)

@app.route("/aws-ec2-instances/")
def instances():
    template = 'aws-ec2-instances.html'
    object_list = get_csv_instances()
    return render_template(template, object_list=object_list)

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
