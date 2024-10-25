from dbtour import dbtour_app
import sqlite3
from flask import render_template, request


@dbtour_app.route("/")
def homePage():
    conn = sqlite3.connect("asmagh_games.db")
    
    #join the two tables together
    cursor = conn.execute("""SELECT games.title, games.rating, 
    games.avgLength, games.releaseDate, games.developer,
    developers.headquartersCity FROM games JOIN developers ON 
    games.developer = developers.name limit 10""")
    gameData = cursor.fetchall();
    
    #grab the developers    
    cursor = conn.execute("""SELECT DISTINCT developer from games join
    developers on games.developer = developers.name limit 10""")
    developers = cursor.fetchall()

    #grab the ratings
    cursor = conn.execute("""SELECT DISTINCT rating from games""")
    ratings = cursor.fetchall()

    return render_template("home.html", gameData = gameData, developers = developers, ratings = ratings) 

@dbtour_app.route("/filtered")
def filtered():
    conn = sqlite3.connect("asmagh_games.db")
    
    developer = request.args['developer']
    rating = request.args['rating']
    cursor = conn.execute("""SELECT games.title, games.rating,
           games.avgLength, games.releaseDate, games.developer,
           developers.headquartersCity FROM games JOIN developers ON
           games.developer = developers.name where games.developer = ?
           and games.rating = ? limit 10""", (developer, rating)) 
    filteredTable = cursor.fetchall()

    return render_template("filtered.html", data = filteredTable)
