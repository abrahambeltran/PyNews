"""Main entrance point for the flask app"""
import json
import sqlite3

from os import environ as env
from urllib.parse import quote_plus, urlencode

from authlib.integrations.flask_client import OAuth
from dotenv import find_dotenv, load_dotenv
from flask import Flask, redirect, render_template, session, url_for, request

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

app = Flask(__name__)
app.secret_key = 'APP_SECRET_KEY'

oauth = OAuth(app)

oauth.register(
    "auth0",
    client_id='9i0W32IvzFc2eodJp8X8LQ3adJmjCulD',
    client_secret='o50GsgaLizuydlJyLTD_UG8JdoBZugOmcEHhDjR7OgrkD232iBU5m_pkL_Ungj2i',
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f'https://dev-ws6kun7d.us.auth0.com/.well-known/openid-configuration'
)

connection = sqlite3.connect('newsinfo.db')
cursor = connection.cursor()
cursor1 = cursor.execute('SELECT theindic,url,title,by,time,id FROM news')
posts = cursor1.fetchall()
cursor3 = cursor.execute('SELECT email,url,title,by,time,like,dislike,likeid FROM userlikes')
cursor3.fetchall()

@app.route("/login")
def login():
    """Login function for authorizing through auth0"""
    return oauth.auth0.authorize_redirect(
        redirect_uri=url_for("callback", _external=True)
    )

@app.route("/callback", methods=["GET", "POST"])
def callback():
    """Callback redirect for login/logout functionality"""
    token = oauth.auth0.authorize_access_token()
    session["user"] = token
    return redirect("/")

@app.route("/logout")
def logout():
    """Logout function for leaving the website"""
    session.clear()
    return redirect(
        "https://" + 'dev-ws6kun7d.us.auth0.com'
        + "/v2/logout?"
        + urlencode(
            {
                "returnTo": url_for("home", _external=True),
                "client_id": '9i0W32IvzFc2eodJp8X8LQ3adJmjCulD',
            },
            quote_via=quote_plus,
        )
    )

@app.route("/")
def home():
    """Main entry point for the home page of the website"""
    cursor1 = cursor.execute('SELECT theindic,url,title,by,time,id FROM news')
    posts = cursor1.fetchall()
    return render_template("home.html", session=session.get('user'),
    pretty=json.dumps(session.get('user'), indent=4), posts=posts)

@app.route("/profile")
def profile():
    """Flask route for profile page using database/auth0 info"""
    cursor3 = cursor.execute('SELECT email,url,title,by,time,like,dislike,likeid FROM userlikes')
    userlikes = cursor3.fetchall()
    return render_template("profile.html", session=session.get('user'),
    pretty=json.dumps(session.get('user'), indent=4), userlikes=userlikes)

@app.route("/delete/<likeid>", methods=['GET', 'POST'])
def delete(likeid):
    """Flask route for deleting a like selection from userlikes table"""
    sql = 'DELETE FROM userlikes WHERE likeid=' + likeid
    connection.execute(sql)
    connection.commit()
    cursor3 = cursor.execute('SELECT email,url,title,by,time,like,dislike,likeid FROM userlikes')
    cursor3.fetchall()
    return admin()

@app.route("/like/<postid>", methods=['GET', 'POST'])
def like(postid):
    """Flask route for liking a post to input to userlikes table"""
    sql = 'SELECT id FROM news WHERE id=' + postid
    likecursor = cursor.execute(sql)
    post = likecursor.fetchall()
    email = request.form.get("email")
    url = request.form.get("url")
    title = request.form.get("title")
    by = request.form.get("by")
    time = request.form.get("time")
    first = 'INSERT or REPLACE INTO userlikes(email, id, url, title, by, time, like) '
    second = 'VALUES (?,?,?,?,?,?,?)'
    insertsql = first + second
    cursorins = connection.execute(insertsql,(email,str(postid),url,title,by,str(time),1))
    connection.commit()
    return home()

@app.route("/dislike/<postid>", methods=['GET', 'POST'])
def dislike(postid):
    """Flask route for liking a post to input to userlikes table"""
    sql = 'SELECT id FROM news WHERE id=' + postid
    likecursor = cursor.execute(sql)
    post = likecursor.fetchall()
    email = request.form.get("email")
    url = request.form.get("url")
    title = request.form.get("title")
    by = request.form.get("by")
    time = request.form.get("time")
    first = 'INSERT or REPLACE INTO userlikes(email, id, url, title, by, time, dislike) '
    second = 'VALUES (?,?,?,?,?,?,?)'
    insertsql = first + second
    cursorins = connection.execute(insertsql,(email,str(postid),url,title,by,str(time),1))
    connection.commit()
    return home()

@app.route("/admin")
def admin():
    """Flask route for admin management page, uses all data from database"""
    cursor2 = cursor.execute('SELECT email,admin FROM useradmin')
    admins = cursor2.fetchall()
    cursor3 = cursor.execute('SELECT email,url,title,by,time,like,dislike,likeid FROM userlikes')
    userlikes = cursor3.fetchall()
    return render_template("admin.html", session=session.get('user'),
    pretty=json.dumps(session.get('user'), indent=4), userlikes=userlikes, admins=admins)

if __name__ == "__main__":
    app.run(host='157.230.11.9', port=env.get("PORT", 3000), debug=True)
