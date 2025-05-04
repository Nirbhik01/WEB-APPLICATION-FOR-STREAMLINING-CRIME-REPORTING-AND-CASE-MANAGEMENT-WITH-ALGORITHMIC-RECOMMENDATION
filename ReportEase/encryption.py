from cryptography.fernet import Fernet
from django.conf import settings
import os

# Load the key from settings or env variable (store securely)
FERNET_KEY = getattr(settings, "FERNET_KEY", None)

if FERNET_KEY is None:
    raise ValueError("FERNET_KEY must be set in settings.py")

fernet = Fernet(FERNET_KEY)

def encrypt_file(file):
    return fernet.encrypt(file.read())

def decrypt_file(file_path):
    with open(file_path, "rb") as f:
        encrypted_data = f.read()
    return fernet.decrypt(encrypted_data)
