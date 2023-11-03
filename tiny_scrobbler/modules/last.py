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

	def __init__(self, api_key, secret_key, session_key=''):
		self.__API_KEY__ = api_key
		self.__SECRET__ = secret_key

		self.keys_are_valid = (len(api_key) == 32) and (len(secret_key) == 32)

		self.__SESSION_KEY__ = session_key
	
	@handle_error
	def get_signed_object(self, data, secret):

		# ordered by keys
		data = [f'{i}{data[i]}' for i in sorted(data.keys())]

		# joined data with secret
		joined_data = ''.join(data) + secret

		sig = md5(joined_data.encode('utf-8')).hexdigest()
		return sig



	@handle_error
	def authorize(self):
		if self.__SESSION_KEY__:
			return
		
		# run server only if not already running one
		if not self.port:
			self.port = try_run_server()

		# desktop auth
		# url = f'http://www.last.fm/api/auth/?api_key={self.__API_KEY__}&token={self.token}'

		# web auth
		url = f'http://www.last.fm/api/auth/?api_key={self.__API_KEY__}&cb=http://127.0.0.1:{self.port}/callback'
		
		webbrowser.open(url, new=0, autoraise=True)
		
		# waiting for token from localhost
		while not config.TOKEN:
			time.sleep(1)

		self.token = config.TOKEN
		self.port = None

	@handle_error
	def get_sk(self):
		if self.__SESSION_KEY__:
			return
		print('token:', self.token)
		if self.token:
			payload = {
				'method': 'auth.getSession',
				'api_key': self.__API_KEY__,
				'token' : self.token
			}

			signature = self.get_signed_object(payload, self.__SECRET__)
			payload['api_sig'] = signature

			response = requests.get(API_BASE, params=as_json(payload))
			
			self.__SESSION_KEY__ = response.json()['session']['key']
			self.user = response.json()['session']['name']

			# token only can be used once
			self.token = None
			
			# save keys with sk encrypted
			load_keys(new_keys={'api_key': self.__API_KEY__,
					   			'secret_key': self.__SECRET__,
					   			'session_key': self.__SESSION_KEY__})
		else:
			raise Exception('Not authorized!')




	# !!!	NOT IN USE	!!! #
	@handle_error
	def request_token(self):
		payload = {
				'method': 'auth.getToken',
				'api_key': self.__API_KEY__,
			}

		response = requests.get(API_BASE, params=as_json(payload))

		if response.status_code == 200:
			# json_data = json.loads(response.data.decode('utf-8'))
			self.token = response.json()['token']
			print('[request token] token:', self.token)
		else:
			raise Exception(f'No token [{str(response.status_code)}]')
	
	# !!!	NOT IN USE	!!! #
	def creds_auth(self):
		payload = {
			'method': 'auth.getMobileSession',
			'api_key': self.__API_KEY__,
			'password': 'PASSWORD',
			'username': 'USERNAME',
		}

		# DEPRECATED
		# user = 'USERNAME'
		# passw = 'PASSWORD'
		# passw = md5(passw.encode('utf-8')).hexdigest()
		# payload['authToken'] = md5((user + passw).encode('utf-8')).hexdigest()

		sig = self.get_signed_object(payload, self.__SECRET__)
		payload['api_sig'] = sig
		response = requests.post(API_BASE, params=as_json(payload))
		print(response.text)
		print(response.url)
		

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
			encrypted_api_keys = config_data["api_keys"].encode()

			decrypted_api_keys = json.loads(encryption.decrypt(encrypted_api_keys, key))
			return decrypted_api_keys
		
	else: 
		
		if new_keys: # load keys from func argument
			api_key = new_keys["api_key"]
			api_secret = new_keys["secret_key"]
			session_key = new_keys["session_key"]
			
		else: # load keys from config.py
			api_key = config.API_KEY
			api_secret = config.API_SECRET
			session_key = config.SESSION_KEY

		key, salt = encryption.generate_key()
		
		encrypted_data = encryption.encrypt(
			json.dumps({"api_key":    api_key, 
						"secret_key": api_secret,
						'session_key': session_key}), key)

		with open(CONFIG_FILE, "w") as file:
			json.dump({"key": key.decode(), 
					"salt": salt.decode(), 
					"api_keys": encrypted_data.decode()}, 
					file)

		print("API keys stored securely!")

lastfm = Lastfm(**load_keys())
