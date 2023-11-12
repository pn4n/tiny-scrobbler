import json
import webbrowser
from hashlib import md5
import requests
import time
import os

from exceptions import handle_error
import config
from localhost import try_run_server
import encryption

API_BASE = 'https://ws.audioscrobbler.com/2.0/'
as_json = lambda x: {**x, **{'format': 'json'}}
CONFIG_FILE = "config.json"

class Lastfm():
	token = None
	port = None

	def __init__(self, api_key, api_secret, session_key=None, username=None):
		self.__API_KEY__ = api_key
		self.__API_SECRET__ = api_secret

		if api_key and api_secret:
			self.keys_are_valid = (len(api_key) == 32) and (len(api_secret) == 32)
		else:
			self.keys_are_valid = False

		self.__SESSION_KEY__ = session_key
		self.username = username
		self.cache = { 'userInfo': None }
	
	@handle_error
	def get_signed_object(self, data, secret):
		data_str = ''.join([f'{i}{data[i]}' for i in sorted(data.keys())]) + secret
		sig = md5(data_str.encode('utf-8')).hexdigest()
		return sig



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

			print(self.username)
			
			# save keys with sk encrypted
			load_keys(new_keys={'api_key': self.__API_KEY__,
					   			'api_secret': self.__API_SECRET__,
					   			'session_key': self.__SESSION_KEY__,
								'username': self.username})
		else:
			raise Exception('Not authorized!')



	@handle_error
	def get_info(self):

		# return "cashed" info if possible
		if not self.cache['userInfo']:
		
			payload = {
				'method': 'user.getinfo',
				'api_key': self.__API_KEY__,
				'username': self.username
			}
			response = requests.get(API_BASE, params=as_json(payload))

			print('[req] getInfo',response.json())

			self.cache['userInfo'] = response.json()['user']
		
		return self.cache['userInfo']
	
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
	
	@handle_error
	def logout(self):
		self.__SESSION_KEY__ = None
		self.username = None
		del self.cache['userInfo']
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
		

def load_keys(new_keys=None):

	if new_keys:
		# remove config file to create new one
		try:
			os.remove(CONFIG_FILE)
		except:
			# file does not exist
			pass

	# check if we have a config file with keys already
	if os.path.exists(CONFIG_FILE):
		with open(CONFIG_FILE, "r") as file:
			config_data = json.load(file)
			key = config_data["key"].encode()
			encrypted_api_keys = config_data["data"].encode()

			decrypted_api_keys = json.loads(encryption.decrypt(encrypted_api_keys, key))
			return decrypted_api_keys
		
	else: 
		
		if new_keys: # load keys from func argument
			data = {
				'api_key': new_keys['api_key'],
				'api_secret': new_keys['api_secret'],
				'session_key': new_keys['session_key'],
				'username': new_keys['username']
			}
			
		else: # load keys from config.py
			data = {
				'api_key': config.API_KEY,
				'api_secret': config.API_SECRET,
				# username and sk should not be recieved from config.py ?
			}

		key, salt = encryption.generate_key()
		
		encrypted_data = encryption.encrypt(
			json.dumps(data), key)

		with open(CONFIG_FILE, "w") as file:
			json.dump({"key": key.decode(), 
					"salt": salt.decode(), 
					"data": encrypted_data.decode()}, 
					file)

		print("API keys stored securely!", encrypted_data)

		print(data)
		return data
	
lastfm = Lastfm(**load_keys())
