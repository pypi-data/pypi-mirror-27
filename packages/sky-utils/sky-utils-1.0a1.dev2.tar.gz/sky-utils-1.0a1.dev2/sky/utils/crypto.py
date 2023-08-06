from cryptography.fernet import Fernet
import base64
import os


def encrypt(key, msg):
    return Fernet(key).encrypt(msg)


def decrypt(key, token):
    return Fernet(key).decrypt(token)


def generate_key():
    return base64.urlsafe_b64encode(os.urandom(32))