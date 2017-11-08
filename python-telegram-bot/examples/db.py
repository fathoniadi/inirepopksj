import sqlite3

db = sqlite3.connect('./permakanin.db')
cursor = db.cursor()
users = cursor.execute('select * from user').fetchall()
print users