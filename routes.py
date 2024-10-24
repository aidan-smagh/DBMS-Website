from dbtour import dbtour_app
import sqlite3

@dbtour_app.route("/")
def does_this_work():
    conn = sqlite3.connect("asmagh_games.db")
    cursor = conn.execute("SELECT * FROM games")
    games = cursor.fetchall()
    return f"<HTML><BODY><H1>{games[0][0]}</H1></BODY></HTML>"
