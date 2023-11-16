import webbrowser
from hashlib import md5
import requests
import time
import threading

from window import handle_error
import config
from localhost import try_run_server
from encryption import load_keys

API_BASE = 'https://ws.audioscrobbler.com/2.0/'
as_json = lambda x: {**x, **{'format': 'json'}}
	

class Lastfm():
	token = None
	port = None
	current_track = None
	__timer_thread__ = None
	__lock__ = threading.Lock()

	def __init__(self, api_key, api_secret, session_key=None, username=None):
		self.__API_KEY__ = api_key
		self.__API_SECRET__ = api_secret

		if api_key and api_secret:
			self.keys_are_valid = (len(api_key) == 32) and (len(api_secret) == 32)
		else:
			self.keys_are_valid = False

		self.__SESSION_KEY__ = session_key
		self.username = username


	@handle_error
	def get_signed_object(self, data, secret):
		data_str = ''.join([f'{i}{data[i]}' for i in sorted(data.keys())]) + secret
		sig = md5(data_str.encode('utf-8')).hexdigest()
		return sig


#___#___#___   AUTH    ___#___#___#


	@handle_error
	def authorize(self):
		if self.username:
			return
		
		# run server only if not already running one
		if not self.port:
			self.port = try_run_server()

		url = f'http://www.last.fm/api/auth/?api_key={self.__API_KEY__}&cb=http://127.0.0.1:{self.port}/callback'
		
		# !!! is used as shared store !!!
		# !     NOT THE BEST OPTION     !
		config.TOKEN = None
		
		webbrowser.open(url, new=0, autoraise=True)
		
		# waiting for token from localhost
		while not config.TOKEN:
			time.sleep(1)

		self.token = config.TOKEN
		self.port = None

	@handle_error
	def get_sk(self):
		if self.username:
			return
		if self.token:
			payload = {
				'method': 'auth.getSession',
				'api_key': self.__API_KEY__,
				'token' : self.token
			}

			signature = self.get_signed_object(payload, self.__API_SECRET__)
			payload['api_sig'] = signature

			response = requests.get(API_BASE, params=as_json(payload))
			
			self.__SESSION_KEY__ = response.json()['session']['key']
			self.username = response.json()['session']['name']

			# token only can be used once
			self.token = None
			
			# save keys with sk encrypted
			load_keys(new_keys={'api_key': self.__API_KEY__,
					   			'api_secret': self.__API_SECRET__,
					   			'session_key': self.__SESSION_KEY__,
								'username': self.username})
		else:
			raise Exception('Not authorized!')

	@handle_error
	def logout(self):
		self.__SESSION_KEY__ = None
		self.username = None
		# del self.cache['userInfo']
		self.token = None

		config.TOKEN = None

		load_keys(new_keys={'api_key': self.__API_KEY__,
					   		'api_secret': self.__API_SECRET__,
							'session_key': None,
							'username': None})

		# # !!!	NOT IN USE	!!! #
		# @handle_error
		# def request_token(self):
		# 	payload = {
		# 			'method': 'auth.getToken',
		# 			'api_key': self.__API_KEY__,
		# 		}

		# 	response = requests.get(API_BASE, params=as_json(payload))

		# 	if response.status_code == 200:
		# 		# json_data = json.loads(response.data.decode('utf-8'))
		# 		self.token = response.json()['token']
		# 		print('[request token] token:', self.token)
		# 	else:
		# 		raise Exception(f'No token [{str(response.status_code)}]')
		
		# # !!!	NOT IN USE	!!! #
		# def creds_auth(self):
		# 	payload = {
		# 		'method': 'auth.getMobileSession',
		# 		'api_key': self.__API_KEY__,
		# 		'password': 'PASSWORD',
		# 		'username': 'USERNAME',
		# 	}

		# 	# DEPRECATED
		# 	# user = 'USERNAME'
		# 	# passw = 'PASSWORD'
		# 	# passw = md5(passw.encode('utf-8')).hexdigest()
		# 	# payload['authToken'] = md5((user + passw).encode('utf-8')).hexdigest()

		# 	sig = self.get_signed_object(payload, self.__API_SECRET__)
		# 	payload['api_sig'] = sig
		# 	response = requests.post(API_BASE, params=as_json(payload))
		# 	print(response.text)
		# 	print(response.url)



#___#___#___   API METHODS    ___#___#___#

	
	@handle_error
	def get_recent(self):

		payload = {
			'method': 'user.getRecentTracks',
			'api_key': self.__API_KEY__,
			'username': self.username,
			'limit': 5
		}
		response = requests.get(API_BASE, params=as_json(payload))

		print(response.json())

		return response.json
	
	def track_info(self):
		payload = {
			'method': 'user.getRecentTracks',
			'api_key': self.__API_KEY__,
			'username': self.username,
			'limit': 5
		}
		response = requests.get(API_BASE, params=as_json(payload))

		print(response.json())

		return response.json

	# @handle_error
	# def get_info(self):

	# 	# return "cashed" info if possible
	# 	if not self.cache['userInfo']:
		
	# 		payload = {
	# 			'method': 'user.getinfo',
	# 			'api_key': self.__API_KEY__,
	# 			'username': self.username
	# 		}
	# 		response = requests.get(API_BASE, params=as_json(payload))

	# 		print('[req] getInfo',response.json())

	# 		self.cache['userInfo'] = response.json()['user']
		
	# 	return self.cache['userInfo']



#___#___#___   SCROBBLING    ___#___#___#

	def on_new_track(self, track_info):
		with self.__lock__:
			if self.__timer_thread__ and self.__timer_thread__.is_alive():
				self.__timer_thread__.cancel()
			
			self.current_track = track_info
			self.__timer_thread__ = threading.Timer(30, self.scrobble_track)
			self.__timer_thread__.start()

	def on_track_stop(self):
		with self.__lock__:
			if self.__timer_thread__ and self.__timer_thread__.is_alive():
				self.__timer_thread__.cancel()
			self.current_track = None
	
	def scrobble_track(self):
		if self.current_track:
			# Perform the call to api
			print(f"Scrobbling: {self.scrobbler.current_track}")
		

	
lastfm = Lastfm(**load_keys())
