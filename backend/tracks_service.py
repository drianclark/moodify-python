#!/usr/bin/env python3

import base64
import json
import logging
import os
from datetime import datetime
from os import access
import dateutil.parser
import requests
import sqlite3
import sys
from flask import Flask, Response, jsonify, redirect, request, url_for
from flask_cors import CORS
from requests.models import StreamConsumedError
from Track import Track

from statistics import mean

logging.basicConfig(level=logging.DEBUG)
app = Flask(__name__)
CORS(app)

client_id = None
client_secret = None

# loading authentication
try:
	with open('authentication.json') as f:
		data = json.load(f)
		client_id = data['client_id']
		client_secret = data['client_secret']
except FileNotFoundError:
	print('No authentication information found')
	sys.exit()
	
try:
	with open('tokens.json') as f:
		data = json.load(f)
		access_token = data['access_token']
		refresh_token = data['refresh_token']

except FileNotFoundError:
	refresh_access_token()


db_time_format = '%Y-%m-%d %H:%M:%S'

@app.before_first_request
def initialize():
	if access_token == None or refresh_token == None:
		print("getting access token")
		code = requests.get('https://accounts.spotify.com/authorize', params={'client_id':client_id, 'response_type':'code', 'redirect_uri':'http://localhost:5000/api/request_token/callback', 'scope':'user-read-recently-played'})

@app.route('/')
def root():
	print("In root")
	return access_token

@app.route('/api/request_token')
def home():
	# get a token from the spotify API
	code = requests.get('https://accounts.spotify.com/authorize', 
				params={'client_id':client_id, 
						'response_type':'code', 
						'redirect_uri':'http://localhost:5000/api/request_token/callback', 
						'scope':'user-read-recently-played'})
	return redirect(code.url)

@app.route('/api/request_token/callback')
def callback():
	global access_token
	global refresh_token

	code = request.args.get('code')
	r = requests.post('https://accounts.spotify.com/api/token', data={'grant_type':'authorization_code', 'code':code, 'redirect_uri':'http://localhost:5000/api/request_token/callback', 'client_id':client_id, 'client_secret':client_secret})
	print(r.json())

	access_token = r.json()['access_token']
	refresh_token = r.json()['refresh_token']

	tokens = {
		'access_token': access_token,
		'refresh_token': refresh_token
	}

	with open('tokens.json') as f:
		json.dump(tokens, f)

	return "Access token is {} and refresh token is {}".format(access_token, refresh_token)

@app.route('/api/update_tracks')
def trigger_tracks_update():
	try:
		new_tracks = update_tracks()
		print("updated tracks")

	except Exception as e:
		print(e)
		return Response(status=400, mimetype='application/json')

	# new_tracks = update_tracks()

	if len(new_tracks) == 0:
		return jsonify([track.asJSON for track in new_tracks]), 204

	else:
		return jsonify([track.asJSON for track in new_tracks])

@app.route('/api/get_tracks_by_days')
def get_tracks_by_days():

	try:
		tracks = []
  
		days = request.args.get('days')
		assert(days.isnumeric())
  
		query = f"""SELECT spotifyid, title, valence, play_date FROM tracks
		WHERE play_date >= date('now','-{days} days') ORDER BY play_date ASC;
		"""
		with sqlite3.connect('../db/test.db') as connection:
			cur = connection.cursor()
			cur.execute(query)  
			queriedTracks = cur.fetchall()
   
		print(queriedTracks)

		for (spotifyid, title, valence, date) in queriedTracks:
			current_track = Track(
				id=spotifyid,
				title=title,
				valence=valence,
				playDate=date
			)
			tracks.append(current_track.asJSON())

	except Exception as e:
		print(e)
		return Response(status=500, mimetype='application/json')

	if len(tracks) == 0:
		return jsonify(tracks), 204
	else:
		return jsonify(tracks), 200


@app.route('/api/get_tracks_by_date')
def get_tracks_by_date():

	try:
		tracks = []

		startDate = request.args.get('startDate')
		endDate = request.args.get('endDate')
  
		assert(isDate(startDate))
		assert(isDate(endDate))

		query = f"""SELECT title, valence, play_date, spotifyid FROM tracks 
  					WHERE play_date BETWEEN '{startDate}' and '{endDate}' 
					ORDER BY play_date ASC;"""

		with sqlite3.connect('../db/test.db') as connection:
			connection.set_trace_callback(print)
			cur = connection.cursor()
			cur.execute(query)
			queriedTracks = cur.fetchall()

		for (title, valence, date, spotifyid) in queriedTracks:
			current_track = Track(
				id=spotifyid,
				title=title,
				valence=valence,
				playDate=date
			)
			tracks.append(current_track.asJSON())

	except Exception as e:
		print(e)
		return Response(status=500, mimetype='application/json')

	if len(tracks) == 0:
		return jsonify(tracks)
	else:
		return jsonify(tracks), 200

@app.route('/api/get_token')
def handle_token_request():
	global access_token
	global refresh_token

	if access_token == None or refresh_token == None:
		return "No access or refresh token. Visit /api/request_token to fetch token"

	try:
		test_request = requests.get('https://api.spotify.com/v1/me/player/recently-played', params={'limit':1}, headers={"Authorization": "Bearer " + access_token}).raise_for_status()

	except requests.exceptions.HTTPError:
		refresh_access_token()

	return jsonify(access_token)

def request_token():
	code = requests.get('https://accounts.spotify.com/authorize', params={'client_id':client_id, 'response_type':'code', 'redirect_uri':'http://localhost:5000/api/request_token/callback', 'scope':'user-read-recently-played'})

def get_recently_played_tracks():
	global access_token

	print('getting tracks')
	response = requests.get(
			 'https://api.spotify.com/v1/me/player/recently-played', 
			params={'limit':50}, 
			headers={"Authorization": "Bearer " + access_token}).json()

	tracks = []
	spotifyIDs = []

	# attempt to get recently played tracks from spotify api, 
	 # if authentication fails, get new access token then retry
	while True:
		try:
			for item in response['items']:	# iterate through all track objects in recently played tracks object
				current_track = Track(
					id=item['track']['id'],
					title=item['track']['name'],
					playDate=item['played_at'],
					valence=0
				)			
				tracks.append(current_track)
						
			spotifyIDs = [track.spotifyID for track in tracks]
			audio_features = requests.get('https://api.spotify.com/v1/audio-features',
												params={'ids':','.join(spotifyIDs)},
												headers={"Authorization": "Bearer " + access_token}).json()['audio_features']
   
			print('entering for loop')
			print(tracks[0])
			for i in range(len(audio_features)):
				tracks[i].acousticness = audio_features[i]['acousticness']
				tracks[i].danceability = audio_features[i]['danceability']
				tracks[i].energy = audio_features[i]['energy']
				tracks[i].speechiness = audio_features[i]['speechiness']
				tracks[i].tempo = audio_features[i]['tempo']
			print('exited for loop')

		except KeyError:
			print("keyerror")
			refresh_access_token()
			response = requests.get(
							'https://api.spotify.com/v1/me/player/recently-played', 
							params={'limit':50}, 
							headers={"Authorization": "Bearer " + access_token}).json()
			continue

		break

	return tracks

def push_tracks_to_db(tracks):
	print('pushing to db')
	for track in tracks:
		track.playDate = to_sql_date_format(track.playDate)
  
	try:
		sql = """INSERT INTO tracks 
		(spotifyid, title, play_date, valence, acousticness, danceability, energy, speechiness, tempo)
		VALUES (?,?,?,?,?,?,?,?,?)"""
  
		tracksInsert = [(
			track.spotifyID,
			track.title,
			track.playDate,
			track.valence,
			track.acousticness,
			track.danceability,
			track.energy,
			track.speechiness,
			track.tempo
		) for track in tracks]
  
		with sqlite3.connect('../db/test.db') as connection:
			cur = connection.cursor()
			cur.executemany(sql, tracksInsert)  
			connection.commit()
   
		print('committed to db')
  
	except Exception as e:
		print(e)

	return tracks

def to_sql_date_format(time):
	datetime_object = dateutil.parser.isoparse(time).replace(tzinfo=None)

	return datetime_object.strftime(db_time_format)

def get_most_recent_play_date_on_db() -> str:

	print('getting date')
	try:
		with sqlite3.connect('../db/test.db') as connection:
			cur = connection.cursor()
			cur.execute('SELECT play_date FROM tracks ORDER BY play_date DESC LIMIT 1;')
   
		date = cur.fetchone()[0] # fetchone() returns a tuple with one element

	except TypeError:
		date = str(datetime.min)

	return date

def isDate(d: str) -> bool:
	try:
		dateutil.parser.parse(d)
		return True
	except:
		return False

def refresh_access_token():
	global refresh_token
	print(refresh_token)

	auth_header = base64.b64encode((client_id + ':' + client_secret).encode('ascii'))
	head = {'Authorization': 'Basic {}'.format(auth_header.decode('ascii'))}
	r = requests.post('https://accounts.spotify.com/api/token', 
				   data={'grant_type': 'refresh_token', 'refresh_token': refresh_token}, 
				   headers=head).json()
 
	tokens = {
		'access_token': r['access_token'],
		'refresh_token': refresh_token
	}
 
	with open('tokens.json', 'w') as f:
		json.dump(tokens, f)

'''
Updating the database:

1. Get the most recent track's (on the database) play date /
2. 1 the most recent tracks from the API, find the overlap with the database track (if it exists)
		if there is overlap:
			only add the more recent tracks
		else:
			add everything
'''

def update_tracks():
	date = datetime.strptime(get_most_recent_play_date_on_db(), db_time_format)
	tracks = get_recently_played_tracks()

	# find the overlap in most recent play date between the fetched tracks and the database items
	index = 0
	for track in tracks:
		datetime_object = dateutil.parser.isoparse(track.playDate).replace(tzinfo=None, microsecond=0) # converting to datetime object (no microsecond or tzinfo) to allow comparison
		# if current track's play date is older than or the same as the most recent in the database, end the loop
		if datetime_object <= date:
			break
		else:
			index += 1

	# get all the tracks that are more recent than the one in the database
	new_tracks = tracks[:index]
	push_tracks_to_db(new_tracks)

	return new_tracks

if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0', port=5000)
