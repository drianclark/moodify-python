from datetime import date
import sqlite3

connection = sqlite3.connect('../db/test.db')
cur = connection.cursor()

testInserts = [('5u8o2GmxD3i5wHYnth4Ux9', 'test1', 0.1, '2020-08-01 19:13:27', 0.2, 0.3, 0.4, 0.5, 0.6)]

sql = "INSERT into tracks VALUES (?,?,?,?,?,?,?,?,?)"

# db.executemany(sql, testInserts)

# db.commit()

# days = 100

# getQuery = f"""SELECT spotifyid, title, valence, play_date FROM tracks
# WHERE play_date >= date('now','-? days') ORDER BY play_date ASC;
# """

dateQuery = "SELECT play_date FROM tracks ORDER BY play_date DESC LIMIT 1;"

startDate = '2020-06-18'
endDate = '2020-09-13'

betweenDatesQuery = f"SELECT title, valence, play_date, spotifyid FROM tracks WHERE play_date BETWEEN '{startDate}' and '{endDate}' ORDER BY play_date ASC;"

cur.execute(betweenDatesQuery)

tracks = cur.fetchall()
print(tracks)