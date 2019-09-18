#!/usr/bin/env python3

from flask import Flask, redirect, request, jsonify
from flask_cors import CORS
import mysql.connector
from datetime import datetime
from dotenv import load_dotenv
import dateutil.parser
import requests
import json
import os
import base64
import logging


logging.basicConfig(level=logging.DEBUG)
logging.getLogger('apscheduler').setLevel(logging.DEBUG)
app = Flask(__name__)
CORS(app)

# loading env variables
load_dotenv()
client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')

# connecting to database
cnx = mysql.connector.connect(user='root', password='admin1', host='db', database='db0')

try:
	access_token = os.getenv('ACCESS_TOKEN')
	refresh_token = os.getenv('REFRESH_TOKEN')

except:
	print("Access token not available, please get one first")

db_time_format = '%Y-%m-%d %H:%M:%S'

# upon application start, get a token
token = requests.get('https://accounts.spotify.com/authorize', params={'client_id':client_id, 'response_type':'code', 'redirect_uri':'http://localhost:5000/', 'scope':'user-read-recently-played'})
redirect(token.url)

# @app.before_first_request
# def initialize():
#

@app.route('/')
def hello_world():

	return access_token

@app.route('/api/request_token')
def home():
	# get a token from the spotify API
	code = requests.get('https://accounts.spotify.com/authorize', params={'client_id':client_id, 'response_type':'code', 'redirect_uri':'http://localhost:5000/api/request_token/callback', 'scope':'user-read-recently-played'})
	print(code.url)

	return redirect(code.url)

@app.route('/api/request_token/callback')
def callback():
	global access_token
	global refresh_token

	code = request.args.get('code')
	r = requests.post('https://accounts.spotify.com/api/token', data={'grant_type':'authorization_code', 'code':code, 'redirect_uri':'http://localhost:5000/api/request_token/callback', 'client_id':client_id, 'client_secret':client_secret})

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

	access_token = os.getenv('ACCESS_TOKEN')
	refresh_token = os.getenv('REFRESH_TOKEN')

	return "Access token is {} and refresh token is {}".format(access_token, refresh_token)

@app.route('/api/update_tracks')
def trigger_tracks_update():
	try:
		new_tracks = update_tracks()

	except:
		return Response(status=400, mimetype='application/json')

	if len(new_tracks) == 0:
		return jsonify(new_tracks), 204

	else:
		return jsonify(new_tracks)

@app.route('/api/get_tracks_by_days')
def get_tracks_by_days():

	try:
		days = request.args.get('days')
		# for now, returns the tracks listened to over the last 48 hours
		tracks = []

		query = """SELECT title, valence, `date`, spotifyid FROM tracks
		WHERE `date` >= now() - INTERVAL (%s) DAY ORDER BY `date` ASC"""

		cur = cnx.cursor()

		cur.execute(query, (days,))

		for (title, valence, date, spotifyid) in cur:
			current_track = {'title':title, 'valence':valence, 'date':date, 'spotifyid':spotifyid}
			tracks.append(current_track)

	except:
		return Response(status=500, mimetype='application/json')

	if len(tracks) == 0:
		return jsonify(tracks), 204
	else:
		return jsonify(tracks), 200


@app.route('/api/get_tracks_by_date')
def get_tracks_by_date():

	try:
		startDate = request.args.get('startDate')
		endDate = request.args.get('endDate')

		tracks = []

		print("before query")

		query = """SELECT title, valence, `date`, spotifyid FROM tracks WHERE
					CAST(`date` as DATE) BETWEEN CAST(%s AS DATE) and CAST(%s AS DATE);"""

		cur = cnx.cursor()
		cur.execute(query, (startDate, endDate,))

		for (title, valence, date, spotifyid) in cur:
			current_track = {'title':title, 'valence':valence, 'date':date, 'spotifyid':spotifyid}
			tracks.append(current_track)

	except:
		return Response(status=500, mimetype='application/json')

	if len(tracks) == 0:
		return jsonify(tracks), 204
	else:
		return jsonify(tracks), 200

@app.route('/api/get_token')
def handle_token_request():
	global access_token

	try:
		test_request = requests.get('https://api.spotify.com/v1/me/player/recently-played', params={'limit':1}, headers={"Authorization": "Bearer " + access_token}).raise_for_status()

	except requests.exceptions.HTTPError:
		refresh_access_token()

	return jsonify(access_token)

def spotify_login():
	# get a token from the spotify API
	token = requests.get('https://accounts.spotify.com/authorize', params={'client_id':client_id, 'response_type':'code', 'redirect_uri':'http://localhost:5000/callback', 'scope':'user-read-recently-played'})

	return redirect(token.url)

def request_token():
	code = requests.get('https://accounts.spotify.com/authorize', params={'client_id':client_id, 'response_type':'code', 'redirect_uri':'http://localhost:5000/api/request_token/callback', 'scope':'user-read-recently-played'})

def get_recently_played_tracks():
	global access_token

	r = requests.get('https://api.spotify.com/v1/me/player/recently-played', params={'limit':50}, headers={"Authorization": "Bearer " + access_token})

	history = r.json()

	tracks = []
	current_track = {}	# empty track object used to add the current track to tracks array

	# attempt to get recently played tracks from spotify api, if authentication fails, get new access token then retry
	while True:
		try:
			print("doing items")
			for item in history['items']:	# iterate through all track objects in recently played tracks object
				# ID
				current_track['id'] = item['track']['id']

				# TITLE
				current_track['title'] = item['track']['name']

				# DATE
				current_track['date'] = item['played_at']

				# AUDIO FEATURES
				audio_features = requests.get('https://api.spotify.com/v1/audio-features/' + item['track']['id'], headers={"Authorization": "Bearer " + access_token}).json()

				current_track['valence'] = audio_features['valence']
				current_track['acousticness'] = audio_features['acousticness']
				current_track['danceability'] = audio_features['danceability']
				current_track['energy'] = audio_features['energy']
				current_track['speechiness'] = audio_features['speechiness']
				current_track['tempo'] = audio_features['tempo']

				# ARTISTS
				# current_track['artists'] = []
				# for artist_object in item['track']['artists']: # iterate through all the artist objects in the artists array
				# 	current_track['artists'].append({'id': artist_object['id'], 'name': artist_object['name'].encode('utf-8')})

				tracks.append(current_track)
				current_track = {} # reset the current track

		except KeyError:
			print("keyerror")
			refresh_access_token()
			r = requests.get('https://api.spotify.com/v1/me/player/recently-played', params={'limit':50}, headers={"Authorization": "Bearer " + access_token})
			history = r.json()
			continue

		break

	return tracks

def push_tracks_to_db(tracks):
	for track in tracks:
		track['date'] = to_sql_date_format(track['date'])

	cur = cnx.cursor()

	sql = """INSERT INTO `tracks` (spotifyid, title, valence, `date`, acousticness, danceability, energy, speechiness, tempo)
	VALUES (%(id)s,%(title)s,%(valence)s,%(date)s,%(acousticness)s,%(danceability)s,%(energy)s,%(speechiness)s,%(tempo)s)"""

	cur.executemany(sql, tracks)
	cnx.commit()
	cur.close()

	print("pushed to db")
	print(tracks)

	return tracks

def to_sql_date_format(time):
	datetime_object = dateutil.parser.isoparse(time).replace(tzinfo=None)

	return datetime_object.strftime(db_time_format)

def get_most_recent_play_date_on_db():
	cur = cnx.cursor()
	cur.execute('SELECT `date` FROM tracks ORDER BY `date` DESC LIMIT 1;')

	try:
		date = cur.fetchone()[0] # fetchone() returns a tuple with one element

	except TypeError:
		date = datetime.min

	return date

def refresh_access_token():
	try:
		access_token = os.getenv('ACCESS_TOKEN')
		refresh_token = os.getenv('REFRESH_TOKEN')

	except:
		print("Access token not available, please get one first")

	auth_header = base64.b64encode((client_id + ':' + client_secret).encode('ascii'))
	head = {'Authorization': 'Basic {}'.format(auth_header.decode('ascii'))}
	print(refresh_token)
	r = requests.post('https://accounts.spotify.com/api/token', data={'grant_type': 'refresh_token', 'refresh_token': refresh_token}, headers=head).json()
	print(r)
	update_tokens(r["access_token"], refresh_token)

def update_tokens(new_access_token, new_refresh_token):
	global access_token
	global refresh_token
	access_token = new_access_token
	refresh_token = new_refresh_token

	envs = open('.env', 'r').read()
	envs_array = envs.split('\n')
	envs_array = ['ACCESS_TOKEN={}'.format(access_token) if 'ACCESS_TOKEN' in e else e for e in envs_array]
	envs_array = ['REFRESH_TOKEN={}'.format(refresh_token) if 'REFRESH_TOKEN' in e else e for e in envs_array]
	envs = '\n'.join(envs_array)

	with open('.env', 'w') as f:
		try:
			f.write(envs)

		except Exception as e:
			print("exception boi")
			print(e)

	load_dotenv()

'''
Updating the database:

1. Get the most recent track's (on the database) play date /
2. Fetch the most recent tracks from the API, find the overlap with the database track (if it exists)
		if there is overlap:
			only add the more recent tracks
		else:
			add everything
'''

def update_tracks():
	if not app.debug or os.environ.get('WERKZEUG_RUN_MAIN') == 'true':
		# raise ValueError("just testing")
		print("updating tracks")

		date = get_most_recent_play_date_on_db()

		tracks = get_recently_played_tracks()

		# find the overlap in most recent play date between the fetched tracks and the database items
		index = 0
		for track in tracks:
			datetime_object = dateutil.parser.isoparse(track['date']).replace(tzinfo=None, microsecond=0) # converting to datetime object (no microsecond or tzinfo) to allow comparison
			# if current track's play date is older than or the same as the most recent in the database, end the loop
			if datetime_object <= date:
				break
			else:
				index += 1

		# get all the tracks that are more recent than the one in the database
		new_tracks = tracks[:index]
		# print(new_tracks)

		push_tracks_to_db(new_tracks)
		# sched.add_job(update_tracks, 'interval', minutes=2)

		return new_tracks

if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0', port=5000)
