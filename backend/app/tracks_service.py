#!/usr/bin/env python3

from flask import Flask, redirect, request
import mysql.connector
from datetime import datetime
import dateutil.parser
import requests
import logging
import json
import sys

app = Flask(__name__)

cnx = mysql.connector.connect(user='root', password='admin1', host='db', database='db')

client_id = '44ef850b66114e6ea1d2fd3c9124af70'
client_secret = 'e597883834244aadb553d9367a56d650'

db_time_format = '%Y-%m-%d %H:%M:%S'

@app.route('/')
def hello_world():
	tracks = get_recently_played_tracks()

	return str(tracks)


@app.route('/api')
def spotify_login():
	# get a token from the spotify API
	token = requests.get('https://accounts.spotify.com/authorize', params={'client_id':client_id, 'response_type':'code', 'redirect_uri':'http://localhost:5000/callback', 'scope':'user-read-recently-played'})

	return redirect(token.url)


@app.route('/callback', methods=['GET', 'POST'])
def get_token():

	code = request.args.get('code')
	r = requests.post('https://accounts.spotify.com/api/token', data={'grant_type':'authorization_code', 'code':code, 'redirect_uri':'http://localhost:5000/callback', 'client_id':client_id, 'client_secret':client_secret})
	access_token = r.json()['access_token']

	# list of recently played track objects
	tracks = get_recently_played_tracks(access_token)

	print((tracks))

	# most recent play date in datetime format
	date = get_most_recent_play_date_on_db()

	# find the overlap in most recent play date between the fetched tracks and the database items
	index = 0
	for track in tracks:
		datetime_object = dateutil.parser.isoparse(track['date']).replace(tzinfo=None, microsecond=0) # converting to datetime object (no microsecond or tzinfo) to allow comparison
		# if current track's play date is older than or the same as the most recent in the database, end the loop
		print(str(datetime_object))
		print(str(date))
		if datetime_object <= date:
			break
		else:
			index += 1

	# get all the tracks that are more recent than the one in the database
	new_tracks = tracks[:index]

	for track in new_tracks:
		track['date'] = to_sql_date_format(track['date'])

	cur = cnx.cursor()

	sql = "INSERT INTO tracks (title, artist, valence, `date`) VALUES (%(title)s,%(artists)s,%(valence)s,%(date)s)"

	cur.executemany(sql, new_tracks)
	cnx.commit()
	cur.close()

	return str(index)


def get_recently_played_tracks(access_token):
	history = requests.get('https://api.spotify.com/v1/me/player/recently-played', params={'limit':50}, headers={"Authorization": "Bearer " + access_token}).json()

	tracks = []

	current_track = {}	# empty track object used to add the current track to tracks array

	for item in history['items']:	# iterate through all track objects in recently played tracks object
		artists = [] # appending current track's artist(s)

		# DATE
		current_track['date'] = item['played_at']

		# TITLE
		current_track['title'] = item['track']['name']

		# ARTISTS
		for artist_object in item['track']['artists']: # iterate through all the artist objects in the artists array
			artists.append(artist_object['name'])

		current_track['artists'] = ', '.join(artists)

		# VALENCE
		track_id = item['track']['id']

		audio_features = requests.get('https://api.spotify.com/v1/audio-features/' + track_id, headers={"Authorization": "Bearer " + access_token}).json()
		valence = audio_features['valence']
		current_track['valence'] = valence

		tracks.append(current_track)

		current_track = {} # reset the current track

	return tracks

def to_sql_date_format(time):
	datetime_object = dateutil.parser.isoparse(time).replace(tzinfo=None)

	return datetime_object.strftime(db_time_format)

def get_most_recent_play_date_on_db():
	cur = cnx.cursor()
	cur.execute('SELECT `date` FROM tracks ORDER BY `date` DESC LIMIT 1;')

	date = cur.fetchone()[0] # fetchone() returns a tuple with one element

	if date == None:
		date = datetime.min

	return date

'''
Updating the database:

1. Get the most recent track's (on the database) play date /
2. Fetch the most recent tracks from the API, find the overlap with the database track (if it exists)
		if there is overlap:
			only add the more recent tracks
		else:
			add everything
'''


if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0', port=5000)
