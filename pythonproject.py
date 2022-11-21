import json
import sqlite3

from flask_crontab import Crontab
from os import environ as env
from urllib.parse import quote_plus, urlencode

from authlib.integrations.flask_client import OAuth
from dotenv import find_dotenv, load_dotenv
from flask import Flask, redirect, render_template, session, url_for, jsonify

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
cursor1 = cursor.execute('SELECT theindic,url,title,by,time FROM news')
posts = cursor1.fetchall()

@app.route("/login")
def login():
    return oauth.auth0.authorize_redirect(
        redirect_uri=url_for("callback", _external=True)
    )

@app.route("/callback", methods=["GET", "POST"])
def callback():
    token = oauth.auth0.authorize_access_token()
    session["user"] = token
    return redirect("/")

@app.route("/logout")
def logout():
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
    cursor1 = cursor.execute('SELECT theindic,url,title,by,time FROM news')
    posts = cursor1.fetchall()
    return render_template("home.html", session=session.get('user'),
    pretty=json.dumps(session.get('user'), indent=4), posts=posts)

@app.route("/profile")
def profile():
    return render_template("profile.html", session=session.get('user'),
    pretty=json.dumps(session.get('user'), indent=4))

@app.route("/delete/<likeid>", methods=['GET', 'POST'])
def delete(likeid):
    sql = 'DELETE FROM userlikes WHERE likeid=' + likeid
    connection.execute(sql)
    connection.commit()
    cursor3 = cursor.execute('SELECT email,url,title,by,time,like,dislike,likeid FROM userlikes')
    cursor3.fetchall()
    return admin()

@app.route("/admin")
def admin():
    cursor2 = cursor.execute('SELECT email,admin FROM useradmin')
    admins = cursor2.fetchall()
    cursor3 = cursor.execute('SELECT email,url,title,by,time,like,dislike,likeid FROM userlikes')
    userlikes = cursor3.fetchall()
    return render_template("admin.html", session=session.get('user'),
    pretty=json.dumps(session.get('user'), indent=4), userlikes=userlikes, admins=admins)

if __name__ == "__main__":
    app.run(host='157.230.11.9', port=env.get("PORT", 3000), debug=True)
