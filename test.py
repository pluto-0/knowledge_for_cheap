import sqlite3


conn = sqlite3.connect('database.db')
cursor = conn.cursor()
command = ('SELECT * FROM wishlists')
cursor.execute(command)
rows = cursor.fetchall()
print(rows)