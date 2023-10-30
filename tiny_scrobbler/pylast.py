import json
import webbrowser
from hashlib import md5
import urllib3

import exceptions
import config

class PyLast():
	__TOKEN__ = ""

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
		url = f'http://ws.audioscrobbler.com/2.0/?\
method=auth.gettoken&\
api_key={self.__API_KEY__}&\
format=json'
		req_response = self.__http__.request('GET', url, headers={'User-Agent' : 'Mozilla/5.0'})
		if req_response.status == 200:
			json_data = json.loads(req_response.data.decode('utf-8'))
			TOKEN = json_data['token']
			self.__TOKEN__ = TOKEN
		return req_response.status

	@exceptions.handle_error
	def authorize(self):
		if not self.__is_authorized__:
			url = f'http://www.last.fm/api/auth/?\
api_key={self.__API_KEY__}&\
token={self.__TOKEN__}'
			# open browser to authorize app
			webbrowser.open(url, new=0, autoraise=True)
			# Make sure authorized
			# self.__is_authorized__ = True

	@exceptions.handle_error
	def start_session(self):
		if self.__is_authorized__:
			data = f"api_key{self.__API_KEY__,}\
methodauth.getSession\
token{self.__TOKEN__}{self.__SECRET__}"\
.encode(encoding='utf-8')
			self.__api_signature__ = md5(data).hexdigest()
			url = f'http://ws.audioscrobbler.com/2.0/?\
method=auth.getSession&\
api_key={self.__API_KEY__}&\
token={self.__TOKEN__}&\
api_sig={self.__api_signature__}&\
format=json'
			req_response = self.__http__.request('GET', url)

			if req_response.status == 200:
				json_data = json.loads(req_response.data.decode('utf-8'))
				session_key = json_data['session']['key']
				self.__SESSION_KEY__ = session_key

				url = f'http://ws.audioscrobbler.com/2.0/?\
method=track.love&\
api_key={self.__API_KEY__}&\
api_sig={self.__api_signature__}&\
sk={self.__SESSION_KEY__}&\
artist=cher&track=believe&format=json'
				req_response = self.__http__.request('POST', url)

				return self.__SESSION_KEY__
			else:
				print("Error with code " + str(req_response.status))

		else:
			print("Not authorized!") 

last = PyLast(config.API_KEY, config.API_SECRET, config.SESSION_KEY)
