import os
import base64
import json
import platform
from hashlib import sha256
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

import config

CONFIG_FILE = "config.json"

def generate_key():
    salt = base64.urlsafe_b64encode(os.urandom(16))
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    hashed_key = sha256(
            f"{platform.version()[-1]}0909{platform.machine()[-1]}|{platform.system()[-1]}".encode('utf-8')
                                ).hexdigest()

    key = base64.urlsafe_b64encode(
        kdf.derive(
            sha256(
                hashed_key.encode('utf-8'))
                .hexdigest()
                .encode('utf-8')))
    
    return key, salt


def encrypt(data, key):
    cipher_suite = Fernet(key)
    encrypted_data = cipher_suite.encrypt(data.encode())
    return encrypted_data


def decrypt(encrypted_data, key):
    cipher_suite = Fernet(key)
    decrypted_data = cipher_suite.decrypt(encrypted_data).decode()
    return decrypted_data


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

			decrypted_api_keys = json.loads(decrypt(encrypted_api_keys, key))
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

		key, salt = generate_key()
		
		encrypted_data = encrypt(json.dumps(data), key)

		with open(CONFIG_FILE, "w") as file:
			json.dump({"key": key.decode(), 
					"salt": salt.decode(), 
					"data": encrypted_data.decode()}, 
					file)

		return data