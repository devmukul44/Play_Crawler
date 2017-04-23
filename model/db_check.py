import mysql.connector
from mysql.connector import Error


def connect():
    try:
        conn = mysql.connector.connect(host='localhost', database='play', user='root', password='root')
        cursor = conn.cursor()

        cursor.execute("CREATE TABLE chk (ID int(10) auto_increment primary key, url varchar(1000) )")

    except Error as e:
        print(e)

    finally:
        conn.close()


if __name__ == '__main__':
    connect()
