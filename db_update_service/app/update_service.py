from time import sleep
from datetime import datetime
import dateutil.parser
import requests
import mysql.connector
import logging

cnx = mysql.connector.connect(user='root', password='admin1', host='db', database='db0')
logging.basicConfig(filename='update_service.log', level=logging.DEBUG)

db_time_format = '%Y-%m-%d %H:%M:%S'

def get_most_recent_play_date_on_db():
	cur = cnx.cursor()
	cur.execute('SELECT `date` FROM tracks ORDER BY `date` DESC LIMIT 1;')

	try:
		date = cur.fetchone()[0] # fetchone() returns a tuple with one element

	except TypeError: # if nothing's been returned, there must be no entries yet
		date = datetime.min

	return date

def get_recently_played_tracks():
	logging.info("GETTING TRACKS")
	access_token = requests.get('http://backend:5000/api/get_token').json()

	r = requests.get('https://api.spotify.com/v1/me/player/recently-played', params={'limit':50}, headers={"Authorization": "Bearer " + access_token})

	history = r.json()

	tracks = []
	current_track = {}    # empty track object used to add the current track to tracks array
	spotifyIDs = []

	# attempt to get recently played tracks from spotify api, if authentication fails, get new access token then retry
	while True:
		try:
			print("doing items")
			for item in history['items']:	# iterate through all track objects in recently played tracks object
				# ID
				current_track['id'] = item['track']['id']
				spotifyIDs.append(current_track['id'])

				# TITLE
				current_track['title'] = item['track']['name']

				# DATE
				current_track['date'] = item['played_at']

				tracks.append(current_track)
				current_track = {} # reset the current track

			print("for finished")
			audio_features_array = requests.get('https://api.spotify.com/v1/audio-features',
												params={'ids':','.join(spotifyIDs)},
												headers={"Authorization": "Bearer " + access_token}).json()['audio_features']
			# print(audio_features_array)
			for i in range(len(audio_features_array)):
				tracks[i]['id'] = audio_features_array[i]['id']
				# if i == 0:
				# 	print(tracks[i])
				# 	print(audio_features_array[i])
				tracks[i]['valence'] = audio_features_array[i]['valence']
				tracks[i]['acousticness'] = audio_features_array[i]['acousticness']
				tracks[i]['danceability'] = audio_features_array[i]['danceability']
				tracks[i]['energy'] = audio_features_array[i]['energy']
				tracks[i]['speechiness'] = audio_features_array[i]['speechiness']
				tracks[i]['tempo'] = audio_features_array[i]['tempo']

		except KeyError:
			print("keyerror")
			refresh_access_token()
			r = requests.get('https://api.spotify.com/v1/me/player/recently-played', params={'limit':50}, headers={"Authorization": "Bearer " + access_token})
			history = r.json()
			continue

		break

	return tracks

def push_tracks_to_db(tracks):
	logging.info("PUSHING TRACKS")
	for track in tracks:
		logging.info("{}: Will push- {}".format(datetime.today(), track['title']))
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

def update_tracks():
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
	while True:
		update_tracks()
		sleep(180)
