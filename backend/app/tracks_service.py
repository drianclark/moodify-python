#!/usr/bin/env python3

from flask import Flask, redirect, request, jsonify
import mysql.connector
from datetime import datetime
from dotenv import load_dotenv
import dateutil.parser
import requests
import json
import os

app = Flask(__name__)
load_dotenv()

cnx = mysql.connector.connect(user='root', password='admin1', host='db', database='db')

client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')

db_time_format = '%Y-%m-%d %H:%M:%S'

token = requests.get('https://accounts.spotify.com/authorize', params={'client_id':client_id, 'response_type':'code', 'redirect_uri':'http://localhost:5000/', 'scope':'user-read-recently-played'})
redirect(token.url)

@app.route('/')
def hello_world():

	# check if there are access and refresh tokens and display them
	# access_token = os.getenv('ACCESS_TOKEN')
	# refresh_token = os.getenv('REFRESH_TOKEN')
	#
	# if access_token != None and refresh_token != None:
	# 	return "Access token is {} and refresh token is {}".format(access_token, refresh_token)
	#
	# else:
	# 	return "No tokens"

	return "welcome home"

@app.route('/api/get_token')
def home():
	# get a token from the spotify API
	token = requests.get('https://accounts.spotify.com/authorize', params={'client_id':client_id, 'response_type':'code', 'redirect_uri':'http://localhost:5000/api/get_token/callback', 'scope':'user-read-recently-played'})

	return redirect(token.url)

@app.route('/api/get_token/callback')
def get_token():

	code = request.args.get('code')
	r = requests.post('https://accounts.spotify.com/api/token', data={'grant_type':'authorization_code', 'code':code, 'redirect_uri':'http://localhost:5000/api/get_token/callback', 'client_id':client_id, 'client_secret':client_secret})

	access_token = r.json()['access_token']
	refresh_token = r.json()['refresh_token']

	# add new or replace tokens

	envs = open('.env', 'r').read()

	# if tokens don't exist, just append the token entries to the env file
	if 'ACCESS_TOKEN' not in envs or 'REFRESH_TOKEN' not in envs:
		print("no envs")
		with open('.env', 'a') as f:
			try:
				f.write('ACCESS_TOKEN={}\n'.format(access_token))
				f.write('REFRESH_TOKEN={}'.format(refresh_token))

			except Exception as e:
				print(e)

	# if tokens exist, replace their entries on the envs variable and write this to the env file
	else:
		print(envs+'\n')
		envs_array = envs.split('\n')
		envs_array = ['ACCESS_TOKEN={}'.format(access_token) if 'ACCESS_TOKEN' in e else e for e in envs_array]
		envs_array = ['REFRESH_TOKEN={}'.format(refresh_token) if 'REFRESH_TOKEN' in e else e for e in envs_array]
		envs = '\n'.join(envs_array)
		print(envs+'\n')

		with open('.env', 'w') as f:
			try:
				f.write(envs)

			except Exception as e:
				print("exception boi")
				print(e)

	load_dotenv()

	# most recent play date in datetime format
	# date = get_most_recent_play_date_on_db()

	# find the overlap in most recent play date between the fetched tracks and the database items
	# index = 0
	# for track in tracks:
	# 	datetime_object = dateutil.parser.isoparse(track['date']).replace(tzinfo=None, microsecond=0) # converting to datetime object (no microsecond or tzinfo) to allow comparison
	# 	# if current track's play date is older than or the same as the most recent in the database, end the loop
	# 	print(str(datetime_object))
	# 	print(str(date))
	# 	if datetime_object <= date:
	# 		break
	# 	else:
	# 		index += 1

	# get all the tracks that are more recent than the one in the database
	# new_tracks = tracks[:index]
	#
	# for track in new_tracks:
	# 	track['date'] = to_sql_date_format(track['date'])
	#
	# cur = cnx.cursor()
	#
	# sql = "INSERT INTO tracks (title, artist, valence, `date`) VALUES (%(title)s,%(artists)s,%(valence)s,%(date)s)"
	#
	# cur.executemany(sql, new_tracks)
	# cnx.commit()
	# cur.close()

	return "Access token is {} and refresh token is {}".format(access_token, refresh_token)

def spotify_login():
	# get a token from the spotify API
	token = requests.get('https://accounts.spotify.com/authorize', params={'client_id':client_id, 'response_type':'code', 'redirect_uri':'http://localhost:5000/callback', 'scope':'user-read-recently-played'})

	return redirect(token.url)

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
