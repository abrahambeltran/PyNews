"""Python script for scraping HN api and putting data into the database"""
import json
import datetime
import sqlite3
import requests

response_API = requests.get('https://hacker-news.firebaseio.com/v0/topstories.json', timeout=1000)
data = response_API.text
parse_json = json.loads(data)
COUNT = 0
info = []
for i in parse_json:
    URL = "https://hacker-news.firebaseio.com/v0/item/" + str(i) + ".json?print=pretty"
    resp = requests.get(URL, timeout=1000)
    jsonthing = resp.json()
    info.append(jsonthing)
    COUNT = COUNT + 1

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
    time INTEGER
)
""")
COUNT = 0
for i in info:
    if 'url' in info[COUNT]:
        info[COUNT]['theindic'] = int(COUNT)
        info[COUNT]['time'] = datetime.datetime.fromtimestamp(info[COUNT]['time'])
        cursor.execute(
            "INSERT or REPLACE INTO news (theindic,id,url,title,by,time) VALUES (:theindic, :id, :url, :title, :by, :time)", info[COUNT]
        )
    COUNT = COUNT + 1

connection.commit()
connection.close()
