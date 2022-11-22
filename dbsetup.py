import sqlite3

# define cursor and connection
connection = sqlite3.connect('newsinfo.db')
cursor = connection.cursor()

#create news table
cursor.execute("""CREATE TABLE IF NOT EXISTS
userlikes(
    likeid INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT,
    id INTEGER UNIQUE,
    url INTEGER,
    title TEXT,
    by TEXT,
    time TEXT,
    like BOOLEAN,
    dislike BOOLEAN
)
""")

cursor.execute("""CREATE TABLE IF NOT EXISTS
useradmin(
    email TEXT PRIMARY KEY,
    admin BOOLEAN
)
""")


connection.commit()
connection.close()
