import sqlite3
# define cursor and connection

connection = sqlite3.connect('newsinfo.db')

cursor = connection.cursor()

#create stores table

cursor.execute("""CREATE TABLE IF NOT EXISTS
news(
    id INTEGER PRIMARY KEY,
    url TEXT,
    title TEXT,
    by TEXT,
    time REAL
    )
""")
cursor.execute(
    "INSERT INTO news (id,url,title,by,time) VALUES (:id, :url, :title, :by, :time)", 
    info
)
print(cursor.fetchone())

connection.commit()
connection.close()
