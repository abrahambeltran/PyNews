import requests
import json
import sqlite3

response_API = requests.get('https://hacker-news.firebaseio.com/v0/topstories.json')
data = response_API.text
parse_json = json.loads(data)
count = 0
info = []
for i in parse_json:
	url = "https://hacker-news.firebaseio.com/v0/item/" + str(i) + ".json?print=pretty"
	resp = requests.get(url)
	jsonthing = resp.json()
	info.append(jsonthing)
	count = count + 1

# define cursor and connection
connection = sqlite3.connect('newsinfo.db')
cursor = connection.cursor()

#create news table
cursor.execute("""CREATE TABLE IF NOT EXISTS
news(
    theindic INTEGER PRIMARY KEY,
    id INTEGER,
    url TEXT,
    title TEXT,
    by TEXT,
    time REAL
)
""")
count = 0
for i in info:
	if 'url' in info[count]:
		info[count]['theindic'] = int(count)
		cursor.execute(
   			"INSERT or REPLACE INTO news (theindic,id,url,title,by,time) VALUES (:theindic, :id, :url, :title, :by, :time)", info[count]
		)
	count = count + 1
print('done')

connection.commit()
connection.close()
