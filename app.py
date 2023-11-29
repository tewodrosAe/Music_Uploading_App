import email
from genericpath import exists
from imp import reload
from importlib.resources import path
import json
from lib2to3.pytree import convert
from logging import NullHandler
import os
from pathlib import Path
import re
import sqlite3
import csv
import json
from io import BytesIO
from urllib import response
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session,jsonify
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime


def Convert(lst):
    res_dct = {lst[i]: lst[i + 1] for i in range(0, len(lst), 2)}
    return res_dct

def path_finder(path):
    return os.path.exists(path)

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

#dir
db = SQL("sqlite:///music.db")

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
def index():
    if session.get("user_id") is None:
        return redirect("/login")
    else:
        user_id = session["user_id"]
        names = db.execute("SELECT * FROM users WHERE id = ?",user_id)
        name = names[0]["username"]
        return render_template("index.html",name=name,Path=Path(f"static/profile pic/{name}.jpg"),path_finder=path_finder)

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "GET":
        if session.get("user_id") is None:
            return render_template("login.html")
        else:
            return redirect("/")
    else:
        name = request.form.get("username")    
        password = request.form.get("password")
        user = db.execute("SELECT * FROM users WHERE username = ?",name)
        if len(user) != 1:
            flash("Wrong password or username!!!",'error') 
            return render_template("login.html")
        if not check_password_hash(user[0]["password"],password):
            flash("Wrong password!!!",'error')
            return render_template("login.html")
        else:
            user_id = user[0]["id"]
            session["user_id"] = user_id
            flash("Succesfully Logged In!",'success')
            return redirect("/")
@app.route("/popular")
def popular():
    user_id = session["user_id"]
    names = db.execute("SELECT * FROM users WHERE id = ?",user_id)
    name = names[0]["username"]
    musics = db.execute("SELECT * FROM upload")
    return render_template("popular.html",name=name,musics=musics,path_finder=path_finder,Path=Path(f"static/profile pic/{name}.jpg"))

@app.route("/register",methods=["POST"])
def register():
    if request.method == "POST":
        name = request.form.get("username")
        password = request.form.get("password")
        hashed = generate_password_hash(password)
        email = request.form.get("email")
        confirm = request.form.get("confirm")
        pattern = re.compile("[A-Za-z0-9]+")
        names = db.execute("SELECT * FROM users WHERE username = ?",name)
        date = datetime.now()
        if not name or not email or not confirm or not password:
            flash("Input space left blank",'error')
            return render_template("login.html")
        if not pattern.fullmatch(name):
            flash("Unsupported username",'error')
            return render_template("login.html")
        if len(names) != 0:
            flash("Error username is taken",'error')
            return render_template("login.html")
        if len(password) < 6:
            flash("Unsupported username",'error')
            return render_template("login.html")
        if password != confirm:
            flash("Password doesnt match",'error')
            return render_template("login.html")
        else:
            db.execute("INSERT INTO users(username,email,password,date) VALUES(?,?,?,?)",name,email,hashed,date)
            user_id = db.execute("SELECT * FROM users WHERE username = ?",name)
            session["user_id"] = user_id[0]["id"]
            return redirect("/")
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/upload", methods=["GET","POST"])
def upload():
    user_id = session["user_id"]
    names = db.execute("SELECT * FROM users WHERE id = ?",user_id)
    if request.method == "GET":
        name = names[0]["username"]
        return render_template("upload.html",name=name,Path=Path(f"static/profile pic/{name}.jpg"),path_finder=path_finder)
    else:
        file = request.files["file"]
        artist =  request.form.get("artist")
        title = request.form.get("music")
        album = request.form.get("album")
        user_id = session["user_id"]
        username = names[0]["username"]
        if not artist or not title or not album or not file :
            return jsonify("ERROR: file or space left empty")
        else: 
            file.save(f'static/music/{title}.mp3')
            db.execute("INSERT INTO upload(artist,album,title,username) VALUES(?,?,?,?)",artist,album,title,username)
            files = {
                        "musician": artist,
                        "title": title
                    } 
            
            # open the json file
            with open ("db.json",'r') as file:
                data = json.load(file)

            # update json file
            data.append(files)   
            json_data = json.dumps(data,indent=1)

            # Add the data 
            with open ("db.json",'w') as file:
                file.write(json_data) 

            return redirect("/")

@app.route("/me", methods=['POST','GET'])
def me():
    user_id = session["user_id"]
    names = db.execute("SELECT * FROM users WHERE id = ?",user_id)
    name = names[0]["username"]
    if request.method == "GET":
        email = names[0]["email"]
        date =  names[0]["date"]
        cash = names[0]["cash"]
        donates =  db.execute("SELECT * FROM donate WHERE user_id = ? ORDER BY date",user_id)
        if len(donates) >= 1:
            donate = donates[0]["donated"]
        else:
            donate = 0
        return render_template("me.html",name=name,email=email,date=date,cash=cash,donate=donate,Path=Path(f"static/profile pic/{name}.jpg"),exists=exists,path_finder=path_finder)
    else:
        file = request.files["profile_pic"]
        if not file:
            flash("ERROR: Image invalid")
            return redirect('/me')
        file.save(f"static/profile pic/{name}.jpg")
        return redirect("/me")

@app.route("/donate", methods=["POST"])
def donate():
    donatee = request.form.get("donate_user")
    password = request.form.get("passwords")
    try:
        amount = float(request.form.get("donated"))
    except (ValueError,TypeError,NameError):
        flash("ERROR: Amount isnt numeric",'error')
        return redirect("/")
    user_id = session["user_id"]
    donates = db.execute("SELECT * FROM users WHERE username = ?",donatee)
    date = datetime.now()
    real_password = db.execute("SELECT * FROM users WHERE id = ?",user_id)
    if not donatee or not password or not amount:
        flash("ERROR: Space left empty",'error')
        return redirect("/")
    else:
        if len(donates) != 1:
           flash("ERROR: User doesn't exist",'error')
           return redirect("/")
        if real_password[0]["username"] == donatee:
            flash("ERROR: You can't donate to yourself",'error')
            return redirect("/")
        if not check_password_hash(real_password[0]['password'],password):
            flash("ERROR: Password is incorrect",'error')
            return redirect("/")
        else:
            donate_id = donates[0]["id"]
            db.execute("INSERT INTO donate(user_id,donate_id,donated,date) VALUES(?,?,?,?)",user_id,donate_id,amount,date)
            cash = real_password[0]['cash']
            changed_cash = cash - amount
            db.execute("UPDATE users SET cash = ? WHERE id = ?",changed_cash,user_id)
            cashs = donates[0]['cash']
            added_cash = cashs + amount
            db.execute("UPDATE users SET cash = ? WHERE id = ?",added_cash,donate_id)
            flash("SUCCESS,Thanks for donating!")
            return redirect("/")

@app.route("/fetch", methods=["GET"])
def fetch():
    musics = db.execute("SELECT * FROM upload")
    data = { music['title']:music['artist'] for music in musics}
    return data

@app.route("/search",methods=["POST"])
def search():
    user_id = session["user_id"]
    names = db.execute("SELECT * FROM users WHERE id = ?",user_id)
    name = names[0]["username"]
    search = request.form.get("search")
    search = '%' + search + '%'
    musics = db.execute("SELECT * FROM upload WHERE artist LIKE ? or title like ? or album like ? or username like ?",search,search,search,search)
    return render_template("search.html",name=name,musics=musics,path_finder=path_finder,Path=Path(f"static/profile pic/{name}.jpg"))

@app.route("/searchUser",methods=["POST"])
def searchuser():
    user_id = session["user_id"]
    names = db.execute("SELECT * FROM users WHERE id = ?",user_id)
    name = names[0]["username"]
    username = request.form.get("user")
    users = db.execute("SELECT * FROM users WHERE username = ?",username)
    nameo = users[0]["username"]
    email = users[0]["email"]
    return render_template("user.html",name=name,names=nameo,email=email,path_finder=path_finder,Path=Path(f"static/profile pic/{name}.jpg"),Paths=Path(f"static/profile pic/{nameo}.jpg"))
   
