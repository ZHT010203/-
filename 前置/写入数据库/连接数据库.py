import pymysql

def connect_db():
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password='123456',
        database='001'
    )
    return conn

