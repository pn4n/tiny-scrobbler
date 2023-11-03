import os
import base64
import json

from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

import platform
import hashlib


def generate_key():
    salt = base64.urlsafe_b64encode(os.urandom(16))
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    hashed_key = hashlib.sha256(
            f"{platform.version()[-1]}0909{platform.machine()[-1]}|{platform.system()[-1]}".encode('utf-8')
                                ).hexdigest()

    key = base64.urlsafe_b64encode(
        kdf.derive(
            hashlib.sha256(
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
