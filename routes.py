from dbtour_dev import dbtour_app
import sqlite3
from flask import render_template, request, url_for
import redis


@dbtour_app.route("/")
def homePage():
    conn = sqlite3.connect("asmagh_games.db")
    r = redis.Redis(db=30, password="BenAndJerrys", decode_responses=True)

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

    #select all games from the table
    cursor = conn.execute("select title from games")
    allGames = cursor.fetchall()
    
    queue = r.lrange("queue:games", 0, -1)

    #get games and the scores
    ranked = r.zrevrange("scores:games", 0, -1, withscores=True)

    return render_template("home.html", gameData = gameData, developers = developers, ratings = ratings, queue = queue, allGames = allGames, ranked=ranked) 

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
    if title == "":
        return "<HTML><BODY>Enter a valid game</BODY><HTML>"
        

    rating=request.args['rating']
    avgLength=request.args['length']
    developer=request.args['developer']
    releaseDate=request.args['releaseDate']
    if releaseDate =="":
        return "<HTML><BODY>Enter a valid game</BODY><HTML>"
    
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
    
    #commit    
    conn.commit() 
    return homePage()

@dbtour_app.route("/addToQueue")
def addToQueue():
     r = redis.Redis(db=30, password="BenAndJerrys", decode_responses=True)
 
     game = request.args['game']
     queue = r.lrange("queue:games", 0, -1)
     for games in queue:
        if game == games:
            return "<HTML><BODY>Game is already in the queue</BODY></HTML>"
     
     listLength = r.llen("queue:games") 
     if (listLength == 3):
        r.rpop("queue:games")
        add = r.rpush("queue:games", game)
     elif (listLength < 3):
        add = r.rpush("queue:games", game)    
      
     if (listLength > 3): 
        r.rpop("queue:games")
     

     return homePage()


@dbtour_app.route("/removeFromQueue")
def removeFromQueue():
    r = redis.Redis(db=30, password="BenAndJerrys", decode_responses=True)
 
    game = request.args['game']
    queue = r.lrange("queue:games", 0, -1)

    
    if game not in queue:        
        return """<HTML><BODY>Can't remove a game not in the queue
        </BODY></HTML>"""

    r.lrem("queue:games", 1, game)

            
    return homePage()

@dbtour_app.route("/addScore")
def addScore():
    r = redis.Redis(db=30, password="BenAndJerrys", decode_responses=True)
    
    game = request.args['game']
    score = float(request.args['score'])
    
    r.zadd("scores:games", {game: score})
    return homePage()
