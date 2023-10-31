import json
import webbrowser
from hashlib import md5
import urllib3
import requests
import threading, time


import exceptions
import config
from localhost import run_server, stop_server

API_BASE = 'https://ws.audioscrobbler.com/2.0/'
as_json = lambda x: {**x, **{'format': 'json'}}

class PyLast():
	__TOKEN__ = ''

	def __init__(self, API_KEY, SECRET, SESSION_KEY=None):
		self.__API_KEY__ = API_KEY
		self.__SECRET__ = SECRET
		self.__SESSION_KEY__ = SESSION_KEY
		self.__api_signature__ = None
		if SESSION_KEY is None:
			self.__is_authorized__ = False
		else:
			self.__is_authorized__ = True

		self.__http__ = urllib3.PoolManager()

	@exceptions.handle_error
	def request_token(self):
		url = f'http://ws.audioscrobbler.com/2.0/?method=auth.gettoken&api_key={self.__API_KEY__}&format=json'
		req_response = self.__http__.request('GET', url, headers={'User-Agent' : 'Mozilla/5.0'})
		if req_response.status == 200:
			json_data = json.loads(req_response.data.decode('utf-8'))
			TOKEN = json_data['token']
			self.__TOKEN__ = TOKEN
			print('got token')
		else:
			raise Exception(f'No token [{str(req_response.status)}]')

	@exceptions.handle_error
	def authorize(self):
		if not self.__is_authorized__:

			port = try_run_server()
			url = f'http://www.last.fm/api/auth/?api_key={self.__API_KEY__}&cb=http://127.0.0.1:{port}/callback'
			# url = f'http://www.last.fm/api/auth/?api_key={self.__API_KEY__}&token={self.__TOKEN__}'
			webbrowser.open(url, new=0, autoraise=True)
			# ?????????
			print('__is_authorized__ check')
			time.sleep(60)
			stop_server()
			self.__is_authorized__ = True

	@exceptions.handle_error
	def start_session(self):
		if self.__is_authorized__:
			print('start')
			# get_session(self.__API_KEY__, self.__SECRET__, self.__TOKEN__)

			payload = {
				'method': 'auth.gettoken',
				'api_key': self.__API_KEY__,
			}

			req_response = requests.post(API_BASE, params=as_json(payload))
			print(req_response.json())

			payload['token'] = req_response.json()['token']
			payload['token'] = self.__TOKEN__
			payload['method'] = 'auth.getSession'
			signed = self.get_signed_object(payload)
			print(signed)

			req_response = requests.get(API_BASE, params=as_json(signed))
			print(req_response.text)
			# keys = sorted(data.keys())
			# param = [k+data[k] for k in keys]
			# param = "".join(param) + self.__SECRET__
			# print(param)


			# # data = f"api_key{self.__API_KEY__,}methodauth.getSession&token{self.__TOKEN__}{self.__SECRET__}"\
			# 	#	.encode(encoding='utf-8')
			# self.__api_signature__ = md5(param.encode(encoding='utf-8')).hexdigest()
			# data['api_sig'] = self.__api_signature__
			
			# param = [k+ '=' + data[k] for k in data.keys()]
			# param = "&".join(param) + self.__SECRET__
			# print(param)

			# url = API_BASE + param
			# req_response = self.__http__.request('GET', url)
			# print(url)
			# print(f'result: {req_response.status}')
			# if req_response.status == 200:
			# 	json_data = json.loads(req_response.data.decode('utf-8'))
			# 	session_key = json_data['session']['key']
			# 	self.__SESSION_KEY__ = session_key

			# 	url = f'http://ws.audioscrobbler.com/2.0/?method=track.love&api_key={self.__API_KEY__}&api_sig={self.__api_signature__}&sk={self.__SESSION_KEY__}&artist=cher&track=believe&format=json'
			# 	req_response = self.__http__.request('POST', url)

			# 	return self.__SESSION_KEY__
			# else:
			# 	print(req_response)
			# 	raise Exception(f'The action cannot be performed [{str(req_response.status)}]')
		else:
			raise Exception('Not authorized!')
		
	@exceptions.handle_error
	def get_signed_object(self, data):
		'''
			Creates hashed API signature and returns signed object for authentication - https://www.last.fm/api/webauth
			Python solution based on the https://stackoverflow.com/a/30626108/14861722 JS/JQuery solution - thanks!
		'''
		signed_signature = ""
		object_keys = []
		signed_object = {}
		hashed_signature = ""
		for k,v in data.items(): # get list of keys from data
			object_keys.append(k)
		object_keys.sort()
		for key in object_keys: # construct the API method signature as described at , Section 6
			signed_signature = signed_signature + key + data[key]
			signed_object[key] = data[key] # make sure object is in same order, just in case
		signed_signature += self.__SECRET__ # secret key needs to appended to end of signature according to API docs
		# escaped_signature = urllib.parse.quote(signed_signature, safe=" ").encode('utf-8')
		escaped_signature = signed_signature.encode('utf-8')
		print('original sig',escaped_signature)
		hashed_signature = md5(escaped_signature).hexdigest()
		signed_object['api_sig'] = hashed_signature
		# signed_object['format'] = "json" # add return format **after** hashing, signature will be invalid otherwise
		return signed_object

	def get_session(self):
		# Parameters dictionary (excluding format)
		params = {
			'method': 'auth.getSession',
			'api_key': self.__API_KEY__,
			'token': self.__TOKEN__,
		}

		# Sort parameters by key
		sorted_params = sorted(params.items())

		# Concatenate key-value pairs
		concatenated = ''.join(['{}{}'.format(k, v) for k, v in sorted_params])

		# Append secret
		sig_string = concatenated + self.__SECRET__

		# Print this out for debugging
		print("Signature String (Before hashing):", sig_string)

		# MD5 hash
		api_sig = md5(sig_string.encode('utf-8')).hexdigest()

		# Add to payload
		params['api_sig'] = api_sig
		params['format'] = 'json'

		response = requests.post(API_BASE, params=params)
		if response.status_code == 200:
			data = response.json()
			if 'session' in data:
				return data['session']
		
		# Print any errors
		print(f"Error: {response.text}")

		# params = {
		#     'method': 'auth.getSession',
		#     'api_key': self.__API_KEY__,
		#     'token': self.__TOKEN__,
		# }

		# # Step 2: Sort parameters by key
		# sorted_params = sorted(params.items())

		# # Step 3: Concatenate key-value pairs
		# concatenated = ''.join(['{}{}'.format(k, v) for k, v in sorted_params])

		# # Step 4: Append secret
		# sig_string = concatenated + self.__SECRET__

		# # Step 5: MD5 hash
		# api_sig = md5(sig_string.encode('utf-8')).hexdigest()

		# # api_sig = md5(
		# # 	f"api_key{self.__API_KEY__}methodauth.getSessiontoken{self.__TOKEN__}{self.__SECRET__}".encode('utf-8')
		# # ).hexdigest()

		# # Define the payload
		# payload = {
		# 	'method': 'auth.getSession',
		# 	'api_key': self.__API_KEY__,
		# 	'token': self.__TOKEN__,

		# 	'api_sig': api_sig,
		# 	'format': 'json'
		# }

		# payload_sorted = {i: payload[i] for i in sorted(payload.keys())}
		# response = requests.get(API_BASE, params=payload_sorted)
		
		# if response.status_code == 200:
		# 	data = response.json()
		# 	if 'session' in data:
		# 		return data['session']
		
		# # Print any errors
		# print(f"Error: {response.text}")
		# return None

last = PyLast(config.API_KEY, config.API_SECRET, config.SESSION_KEY)

# print(last.request_token())

# last.authorize()
# last.get_session()


@exceptions.handle_error
def try_run_server():
	start_port = 8000
	end_port = 10000

	for i in range(start_port, end_port):
		try:
			t = threading.Thread(target=run_server, args=(i,))
			t.start()
			return i
		except OSError:
			if i == end_port:
				raise Exception(f'No available port[8000-10000]')