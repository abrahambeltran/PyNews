
import requests
import sqlite3



def create_news_db():
    
    news_db = sqlite3.connect("news_db.sqlite")
    c = news_db.cursor()

    #get the count of tables with the name
    c.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='news' ''')

    #if the count is 0, then table does not exists, hence create table
    if c.fetchone()[0]==0 : 
        create_cmd = """CREATE table news
        (news_id integer primary key, 
        title text, 
        author text, 
        url text, 
        like integer, 
        dislike integer)"""

        c.execute(create_cmd)
        news_db.commit()
        
    # Insert news from Hacker News API to the database
    insert_cmd = "INSERT into news values (?, ?, ?, ?, ?, ?)"

    #Make an API call and store the response
    url='https://hacker-news.firebaseio.com/v0/showstories.json'
    r=requests.get(url)
    submission_ids=r.json()

    news_count = 0   # Track the count on news
    index = 0        # index to iterate over submission_ids

    # Collect the top 20 stories and insert to news database
    while news_count <= 20:
        #Make a seperate api call for each id
        url1=f"https://hacker-news.firebaseio.com/v0/item/{submission_ids[index]}.json?print=pretty"
        index += 1
        r1=requests.get(url1)
        response_dict=r1.json()

        # Store only those news with URL
        if 'url' in response_dict:
            row = [response_dict['id'], response_dict['title'], response_dict['by'], response_dict['url'], 0, 0]
            c.execute(insert_cmd, row)
            news_count += 1

    news_db.commit()
    news_db.close()


def show_news():
    
    news_db = sqlite3.connect("news_db.sqlite")
    c = news_db.cursor()

    select_cmd = """SELECT * from news 
    order by like desc 
    limit 20"""

    c.execute(select_cmd)
    news_db.close()

    
def update_news_response(news_id, response_state):
    
    news_db = sqlite3.connect("news_db.sqlite")
    c = news_db.cursor()

    # Response is Like
    if response_state == "Like":
        c.execute("UPDATE news set like = like + 1 where news_id = ?", news_id)
    # Response is Dislike
    else if response_state == "Dislike":
        c.execute("UPDATE news set dislike = dislike + 1 where news_id = ?", news_id)
    # Response is changed to Like from Dislike
    else if response_state == "Dislike to Like":
        c.execute("UPDATE news set like = like + 1, dislike = dislike - 1 where news_id = ?", news_id)
    # Response is changed to Dislike from Like
    else if response_state == "Like to Dislike":
        c.execute("UPDATE news set like = like - 1, dislike = dislike + 1 where news_id = ?", news_id)
    
    news_db.commit()
    news_db.close()

def create_user_db():

    news_db = sqlite3.connect("news_db.sqlite")
    c = news_db.cursor()

    #get the count of tables with the name
    c.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='users' ''')

    #if the count is 0, then table does not exists, hence create table
    if c.fetchone()[0]==0 : 
        create_cmd = """CREATE table users
        (user_id text primary key, 
        name text)"""

        c.execute(create_cmd)
        news_db.commit()
    news_db.close()
    
def insert_user(user_id,name):
    news_db = sqlite3.connect("news_db.sqlite")
    c = news_db.cursor()

    row = [user_id,name]

    c.execute("""INSERT into users values(?,?) """,row)

def create_admin_db(user_id,name):

    news_db = sqlite3.connect("news_db.sqlite")
    c = news_db.cursor()

    #get the count of tables with the name
    c.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='admin' ''')

    #if the count is 0, then table does not exists, hence create table
    if c.fetchone()[0]==0 : 
        create_cmd = """CREATE table admin
        (user_id text references users(user_id), 
        name text references users(name))"""

        c.execute(create_cmd)
        news_db.commit()

    row = [user_id,name]
    c.execute("""INSERT into admin values(?,?) """, row)
    news_db.commit()

    news_db.close()

def create_user_response_db():

    news_db = sqlite3.connect("news_db.sqlite")
    c = news_db.cursor()

    #get the count of tables with the name
    c.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='user_response' ''')

    #if the count is 0, then table does not exists, hence create table
    if c.fetchone()[0]==0 : 
        create_cmd = """CREATE table user_response
        (user_id text references users(user_id),
        news_id integer references news(news_id), 
        IsLike boolean)"""

        c.execute(create_cmd)
        news_db.commit()
    news_db.close()

def update_user_response(user_id, news_id, res):

    news_db = sqlite3.connect("news_db.sqlite")
    c = news_db.cursor()

    c.execute("SELECT count(user_id) FROM user_response WHERE user_id = ? AND news_id = ?", (user_id, news_id))

    if c.fetchone()[0] == 0:
        update_news_response(news_id, res)
        if res == "Like": 
            c.execute(""" INSERT into user_response values(?,?,?)""", [user_id, news_id, True])
        else:
            c.execute(""" INSERT into user_response values(?,?,?)""", [user_id, news_id, False])

    else:
        for response in c.execute("SELECT * from user_response WHERE user_id = ? AND news_id = ?", (user_id, news_id)):
            if response[2] == True and res == "Like":
                return
            else if response[2] == True and res == "Dislike":
                update_news_response(news_id, "Like to Dislike")
                c.execute("UPDATE user_response set IsLike=False where news_id=? and user_id=?",news_id,user_id)

            else if response[2] == False and res == "Like":
                update_news_response(news_id, "Dislike to Like")
                c.execute("UPDATE user_response set IsLike=True where news_id=? and user_id=?",news_id,user_id)

            else if response[2] == False and res == "Dislike":
                return







    
        
    

