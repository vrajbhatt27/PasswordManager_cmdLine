import json
from cryptography.fernet import Fernet
from art import *
import os

path = 'C:\\Users\\91982\\Desktop\\Jarvis\\Python\\Python Projects\\pwd manager'

encrypted = False


class Security:
    def __init__(self, key):
        self.key = key

    def encrypt_data(self, data):
        if isinstance(data, bytes):
            pass
        else:
            data = data.encode()

        f = Fernet(self.key)

        cipher = f.encrypt(data)
        return cipher

    def decrypt_data(self, data):
        f = Fernet(self.key)
        return f.decrypt(data)

# # secondary key (for encryption of main key or promary key)
# seckey = b'9AYbaPTk8FLtXfTXLhF1GFWcAF_m6Eh859O9e_VQAYU='

# primary symmetric key - (main)


def setPrimaryKey():
    global encrypted
    key = Fernet.generate_key()

    with open(os.path.join(path, 'key.pem'), 'wb') as f:
        f.write(key)

    print('New key set')
    encrypted = True


def encrypt_json():
    with open(os.path.join(path, 'data.json'), 'rb') as f:
        data = f.read()

    with open(os.path.join(path, 'key.pem'), 'r') as f:
        key = f.read()

    s = Security(key)
    enc_data = s.encrypt_data(data)

    with open(os.path.join(path, 'data.json'), 'wb') as f:
        f.write(enc_data)


def decrypt_json():
    with open(os.path.join(path, 'data.json'), 'rb') as f:
        data = f.read()

    with open(os.path.join(path, 'key.pem'), 'r') as f:
        key = f.read()

    s = Security(key)

    dec_data = s.decrypt_data(data)

    with open(os.path.join(path, 'data.json'), 'wb') as f:
        f.write(dec_data)


if __name__ == "__main__":
    print('\n')
    tprint("pswd\nManager", "larry3D-xlarge")
    setPrimaryKey()
    if encrypted == True:
        encrypt_json()


# setPrimaryKey()
# encrypt_json()
# decrypt_json()
