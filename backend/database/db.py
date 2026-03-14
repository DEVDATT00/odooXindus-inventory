import pymysql

def get_connection():

    connection = pymysql.connect(
        host="localhost",
        user="root",
        password="",
        database="inventory_db",
        cursorclass=pymysql.cursors.DictCursor
    )

    return connection