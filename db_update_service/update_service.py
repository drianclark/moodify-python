from time import clock_getres, sleep
from json import JSONDecodeError
import requests

print("establishing connection to backend...")

while True:
	try:
		new_tracks = requests.get('http://backend:5000/api/update_tracks', timeout=3).json()
  
	except TimeoutError:
		print("retrying...")
		sleep(3)
		continue
	
	except JSONDecodeError:
		print(f'database updated: no new tracks')
		new_tracks = []
		sleep(900)

	print(f'database updated: {new_tracks}')
	new_tracks = []
	sleep(900)
