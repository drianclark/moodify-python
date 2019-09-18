from time import sleep
import dateutil.parser
import requests
import mysql.connector

cnx = mysql.connector.connect(user='root', password='admin1', host='db', database='db0')

def get_most_recent_play_date_on_db():
    cur = cnx.cursor()
    cur.execute('SELECT `date` FROM tracks ORDER BY `date` DESC LIMIT 1;')

    try:
        date = cur.fetchone()[0] # fetchone() returns a tuple with one element

    except TypeError: # if nothing's been returned, there must be no entries yet
        date = datetime.min

    return date

def get_recently_played_tracks():
    access_token = requests.get('http://backend:5000/api/get_token').json()

    r = requests.get('https://api.spotify.com/v1/me/player/recently-played', params={'limit':50}, headers={"Authorization": "Bearer " + access_token})

    history = r.json()

    tracks = []
    current_track = {}    # empty track object used to add the current track to tracks array

    # attempt to get recently played tracks from spotify api, if authentication fails, get new access token then retry
    while True:
        try:
            print("doing items")
            for item in history['items']:    # iterate through all track objects in recently played tracks object
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
                #     current_track['artists'].append({'id': artist_object['id'], 'name': artist_object['name'].encode('utf-8')})

                tracks.append(current_track)
                current_track = {} # reset the current track

        except KeyError:
            print("keyerror")
            access_token = requests.get('http://backend:5000/api/get_token')
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
