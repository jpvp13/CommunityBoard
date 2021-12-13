import mysql.connector
# from flask_mysqldb import MySQL


mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    passwd = "0000",
)

my_cursor = mydb.cursor()



my_cursor.execute("CREATE DATABASE newDB")

# my_cursor.execute("SHOW DATBASES")
for db in my_cursor:
    print(db)