from time import sleep
import requests

print("establishing connection to backend...")

while True:
	try:
		new_tracks = requests.get('http://backend:5000/api/update_tracks', timeout=3).json()
	except:
		print("retrying...")
		sleep(3)
		continue

	print(f'database updated: {new_tracks}')
	new_tracks = []
	sleep(900)
