from time import clock_getres, sleep
from json import JSONDecodeError
import requests

print("establishing connection to backend...")

while True:
	try:
		new_tracks = requests.get('http://backend:5000/api/update_tracks', timeout=3).json()
  
	except TimeoutError:
		print("Retrying...")
		sleep(3)
		continue
	
	except JSONDecodeError:
		print(f'Database updated: no new tracks')
		new_tracks = []
		sleep(900)
  
	else:
		print('*' * 20)
		print(f'Database updated!')
		print(f"Added {len(new_tracks)} new tracks")
		print()
		print(f"Most recent tracks:")
		print('\n'.join([f'"{track["title"]}" played at {track["playDate"]}' for track in new_tracks[:5]]))
		print('*' * 20)
		print()

 
	new_tracks = []
	sleep(900)

