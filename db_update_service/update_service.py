from time import sleep
from json import JSONDecodeError
import logging
import requests


logger = logging.getLogger('update_service')
logger.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

fileHandler = logging.FileHandler('update_service.log')
fileHandler.setLevel(logging.INFO)
consoleHandler = logging.StreamHandler()
consoleHandler.setLevel(logging.INFO)

logger.addHandler(fileHandler)
logger.addHandler(consoleHandler)

logger.info("establishing connection to backend...")

while True:
	try:
		new_tracks = requests.get('http://backend:5000/api/update_tracks', timeout=3).json()
  
	except (TimeoutError, requests.exceptions.ReadTimeout):
		logger.warn("Timed out")
		logger.info("Retrying...")
		sleep(10)
		continue
	
	except JSONDecodeError:
		logger.info(f'Database updated: no new tracks')
		new_tracks = []
		sleep(900)
  
	else:
		logger.info('*' * 20)
		logger.info(f'Database updated!')
		logger.info(f"Added {len(new_tracks)} new tracks")
		logger.info()
		logger.info(f"Most recent tracks:")
		logger.info('\n'.join([f'"{track["title"]}" played at {track["playDate"]}' for track in new_tracks[:5]]))
		logger.info('*' * 20)
		logger.info()

 
	new_tracks = []
	sleep(900)

