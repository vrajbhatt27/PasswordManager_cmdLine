import json
from cryptography.fernet import Fernet
from art import *
import os




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

def setPrimaryKey():
    key = Fernet.generate_key()

    with open(os.path.join(os.getcwd(), 'key.pem'), 'wb') as f:
        f.write(key)

    print('New key set')


def encrypt_json(data):
    path = os.path.join(os.getcwd(), 'key.pem')

    if(os.path.exists(path)):
        pass
    else:
        setPrimaryKey()


    with open(path, 'r') as f:
        key = f.read()

    s = Security(key)
    enc_data = s.encrypt_data(data)

    return enc_data.decode()


def decrypt_json(data):
    data = data.encode()
    with open(os.path.join(os.getcwd(), 'key.pem'), 'r') as f:
        key = f.read()

    s = Security(key)

    dec_data = s.decrypt_data(data)

    return dec_data.decode()


if __name__ == "__main__":
    print('\n')
    # tprint("pswd\nManager", "larry3D-xlarge")