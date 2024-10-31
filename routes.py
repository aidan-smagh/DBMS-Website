from dbtour import dbtour_app
import sqlite3
from flask import render_template, request, url_for


@dbtour_app.route("/")
def homePage():
    conn = sqlite3.connect("asmagh_games.db")
    
    #join the two tables together
    cursor = conn.execute("""SELECT games.title, games.rating, 
    games.avgLength, games.releaseDate, games.developer,
    developers.headquartersCity FROM games JOIN developers ON 
    games.developer = developers.name order by games.ROWID desc limit 10""")
    gameData = cursor.fetchall();
    
    #grab the developers    
    cursor = conn.execute("""SELECT DISTINCT developer from games join
    developers on games.developer = developers.name""")
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
    if developer == 'all' and rating != 'all':
        cursor = conn.execute("""SELECT games.title, games.rating,
            games.avgLength, games.releaseDate, games.developer,
            developers.headquartersCity FROM games JOIN developers ON
            games.developer = developers.name WHERE games.rating = ?
            limit 10""", (rating,))
        filteredTable = cursor.fetchall()
        return render_template("filtered.html", data = filteredTable) 
    
    elif developer != 'all' and rating == 'all':
        cursor = conn.execute("""select games.title, games.rating, 
                games.avgLength, games.releaseDate, games.developer, 
                developers.headquartersCity from games join developers on 
                games.developer = developers.name where games.developer = ?
                limit 10""", (developer,))
        filteredTable = cursor.fetchall()
        return render_template("filtered.html", data = filteredTable) 
    
    elif developer == 'all' and rating == 'all':
        cursor = conn.execute("""select games.title, games.rating,
           games.avgLength, games.releaseDate, games.developer,
           developers.headquartersCity from games join developers on
           games.developer = developers.name limit 10""")
        filteredTable = cursor.fetchall()
        return render_template("filtered.html", data = filteredTable)
    cursor = conn.execute("""SELECT games.title, games.rating,
           games.avgLength, games.releaseDate, games.developer,
           developers.headquartersCity FROM games JOIN developers ON
           games.developer = developers.name where games.developer = ?
           and games.rating = ? limit 10""", (developer, rating)) 
    filteredTable = cursor.fetchall()

    return render_template("filtered.html", data = filteredTable)

@dbtour_app.route("/addData")
def addData():
    return render_template("addData.html")

@dbtour_app.route("/adding")
def adding():
    conn = sqlite3.connect("asmagh_games.db")

    title=request.args['title']
    rating=request.args['rating']
    avgLength=request.args['length']
    developer=request.args['developer']
    releaseDate=request.args['releaseDate']
    headquarters=request.args['headquarters']

    try:
        cursor = conn.execute("""insert into games (title, rating, avgLength
        , developer, releaseDate) values (?, ?, ?, ?, ?)""", (title, rating,
         avgLength, developer, releaseDate))
    except sqlite3.IntegrityError as e:
        return "<HTML><BODY>Please try again</BODY></HTML>"
    
    cursor = conn.execute("select distinct name from developers")
    check = cursor.fetchall()
    
    for developers in check:
        if developer == developers[0]:
            conn.commit()
            return homePage()
    try:
        cursor = conn.execute("""insert into developers (name, foundingYear,
        headquartersCity) values (?, null, ?)""", (developer, headquarters))
    except sqlite3.IntegrityError as e:
        return "<HTML><BODY>Please try again developers</BODY></HTML>"
    conn.commit() 
    return homePage()
