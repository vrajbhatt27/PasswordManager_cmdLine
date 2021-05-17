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


class Alias:
    def __init__(self):
        if os.path.exists(os.path.join(os.getcwd(), 'settings.json')) == False:
            with open(os.path.join(os.getcwd(), 'settings.json'), 'w') as f:
                data = {'alias': {}}
                json.dump(data, f, ensure_ascii=True, indent=2)

        f = open(r'./settings.json')
        self.settings = json.load(f)
        self.map = self.settings['alias']
        f.close()

    def setAlias(self, name, value):
        try:
            self.map[name] = value
            self.settings['alias'] = self.map
            with open("./settings.json", "w") as f:
                json.dump(self.settings, fp=f, ensure_ascii=True, indent=2)

            print("Alias Added.")
        except:
            print("Some Error Occured while setting the Alias !!!")

    def getAliasValue(self, alias):
        if alias in self.map:
            return self.map[alias]
        else:
            print("Alias Not Present !!!")
            return None

    def removeAlias(self, name):
        try:
            self.map.pop(name)
            self.settings['alias'] = self.map
            with open("./settings.json", "w") as f:
                json.dump(self.settings, fp=f, ensure_ascii=True, indent=2)

            print(f"Alias {name} removed succesfully.")
        except:
            if name not in self.map:
                print("Alias Not present !!!")
            else:
                print("Failed to remove Alias !!!")

    def getAliasList(self):
        ind = 0
        if len(self.map) > 0:
            for k, v in self.map.items():
                print(f"[{ind}] {k} : {v}")
                ind += 1
        else:
            print("No Alias Present !!!")


if __name__ == "__main__":
    print('\n')
    # tprint("pswd\nManager", "larry3D-xlarge")
    al = Alias()
    al.getAliasList()
