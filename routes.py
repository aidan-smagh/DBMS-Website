from dbtour import dbtour_app
import sqlite3
from flask import render_template

@dbtour_app.route("/")
def does_this_work():
    conn = sqlite3.connect("asmagh_games.db")
    
    cursor = conn.execute("SELECT title FROM games")
    titles = cursor.fetchall()

    cursor = conn.execute("SELECT rating FROM games")
    ratings = cursor.fetchall()

    return render_template("home.html", titles = titles, ratings = ratings) 
