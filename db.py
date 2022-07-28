import sqlite3

conn = sqlite3.connect("database.db")

print("opened database successfully")

conn.execute("CREATE TABLE orders (title TEXT, price NUMERIC, imageURL TEXT, qty NUMERIC, sizeLabel TEXT, rowID INTEGER PRIMARY KEY AUTOINCREMENT)")

print("table created successfully")

conn.close()