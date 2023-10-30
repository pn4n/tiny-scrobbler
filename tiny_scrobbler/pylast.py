import json
import webbrowser
from hashlib import md5
import urllib3
import requests


import exceptions
import config

API_BASE = 'http://ws.audioscrobbler.com/2.0/'

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
		else:
			raise Exception(f'No token [{str(req_response.status)}]')

	@exceptions.handle_error
	def authorize(self):
		if not self.__is_authorized__:
			url = f'http://www.last.fm/api/auth/?api_key={self.__API_KEY__}&token={self.__TOKEN__}'
			webbrowser.open(url, new=0, autoraise=True)
			# ?????????
			print('__is_authorized__ check')
			self.__is_authorized__ = True

	@exceptions.handle_error
	def start_session(self):
		if self.__is_authorized__:
			data = {"api_key": self.__API_KEY__,
                    "method": "auth.getSession",
                    "token" : self.__TOKEN__,
                    # "artist" :"coldplay",
                    # "sk" : self.SESSION_KEY
                    }
			print(get_session(self.__API_KEY__, self.__SECRET__, self.__TOKEN__))
			keys = sorted(data.keys())
			param = [k+data[k] for k in keys]
			param = "".join(param) + self.__SECRET__
			print(param)


			# data = f"api_key{self.__API_KEY__,}methodauth.getSession&token{self.__TOKEN__}{self.__SECRET__}"\
				#    .encode(encoding='utf-8')
			self.__api_signature__ = md5(param.encode(encoding='utf-8')).hexdigest()
			data['api_sig'] = self.__api_signature__
			
			param = [k+ '=' + data[k] for k in data.keys()]
			param = "&".join(param) + self.__SECRET__
			print(param)

			url = API_BASE + param
			req_response = self.__http__.request('GET', url)
			print(url)
			print(f'result: {req_response.status}')
			if req_response.status == 200:
				json_data = json.loads(req_response.data.decode('utf-8'))
				session_key = json_data['session']['key']
				self.__SESSION_KEY__ = session_key

				url = f'http://ws.audioscrobbler.com/2.0/?method=track.love&api_key={self.__API_KEY__}&api_sig={self.__api_signature__}&sk={self.__SESSION_KEY__}&artist=cher&track=believe&format=json'
				req_response = self.__http__.request('POST', url)

				return self.__SESSION_KEY__
			else:
				print(req_response)
				raise Exception(f'The action cannot be performed [{str(req_response.status)}]')
		else:
			raise Exception('Not authorized!')

last = PyLast(config.API_KEY, config.API_SECRET, config.SESSION_KEY)



def get_session(api_key, secret, token):
    """
    Fetch a session key using the provided API key, shared secret, and token.
    
    Parameters:
    - api_key: The API key provided by Last.fm for your application
    - secret: The shared secret provided by Last.fm for your application
    - token: The token received after user authorization
    
    Returns:
    - A dictionary with session data or None if an error occurred.
    """

    # Calculate the API signature
    api_sig = md5(
        f"api_key{api_key}methodauth.getSessiontoken{token}{secret}".encode('utf-8')
    ).hexdigest()

    # Define the payload
    payload = {
        'method': 'auth.getSession',
        'api_key': api_key,
        'token': token,
        'api_sig': api_sig,
        'format': 'json'
    }

    # Make the request
    response = requests.post(API_BASE, data=payload)
    
    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        if 'session' in data:
            return data['session']
    
    # Print any errors
    print(f"Error: {response.text}")
    return None