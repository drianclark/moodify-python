#!/usr/bin/env python3

from flask import Flask, redirect, request
from flask_mysqldb import MySQL
import requests
import json
import sys

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'db'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'admin1'
app.config['MYSQL_DB'] = 'db'
# app.config['MYSQL_PORT'] = 3306

mysql = MySQL(app)


@app.route('/')
def hello_world():
	cur = mysql.connection.cursor()
	cur.execute('''SELECT * FROM tracks LIMIT 50''')
	rv = cur.fetchall()

	return str(rv)


@app.route('/api', methods=['GET', 'POST'])
def spotify_login():
	client_id = '44ef850b66114e6ea1d2fd3c9124af70'
	client_secret = 'e597883834244aadb553d9367a56d650'

	# get a token from the spotify API
	token = requests.get('https://accounts.spotify.com/authorize', params={'client_id':client_id, 'response_type':'code', 'redirect_uri':'http://localhost:5000/callback', 'scope':'user-read-recently-played'})

	return redirect(token.url)


@app.route('/callback', methods=['GET', 'POST'])
def get_token():
	client_id = '44ef850b66114e6ea1d2fd3c9124af70'
	client_secret = 'e597883834244aadb553d9367a56d650'

	code = request.args.get('code')
	r = requests.post('https://accounts.spotify.com/api/token', data={'grant_type':'authorization_code', 'code':code, 'redirect_uri':'http://localhost:5000/callback', 'client_id':client_id, 'client_secret':client_secret})
	access_token = r.json()['access_token']

	history = requests.get('https://api.spotify.com/v1/me/player/recently-played', params={'limit':50}, headers={"Authorization": "Bearer " + access_token}).json()

	tracks = []

	current_track = {'artists':[]}	# empty track object used to add the current track to tracks array
	for item in history['items']:	# iterate through all track objects in recently played tracks object

		current_track['date'] = item['played_at']

		current_track['name'] = item['track']['name']

		for artist_object in item['track']['artists']: # iterate through all the artist objects in the artists array
			current_track['artists'].append(artist_object['name'])
		tracks.append(current_track)

		# fetch audio features for each track to get valence
		track_id = item['track']['id']

		audio_features = requests.get('https://api.spotify.com/v1/audio-features/' + track_id, headers={"Authorization": "Bearer " + access_token}).json()
		valence = audio_features['valence']
		current_track['valence'] = valence

		current_track = {'artists':[]} # reset the current track

	return str(tracks)


if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0', port=5000)
