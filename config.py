import json
from cryptography.fernet import Fernet
from art import *
import os
import hashlib
from getpass import getpass


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


class Configure:
    def __init__(self):
        self.settings = None
        if os.path.exists("./settings.json"):
            f = open("./settings.json", "r")
            self.settings = json.load(f)
            f.close()
        else:
            data = {"alias": {}, "pass": ""}
            with open("./settings.json", "w") as f:
                json.dump(data, f, ensure_ascii=True, indent=2)
            self.settings = data

        self.map = self.settings['alias']

    def writeTofile(self, data):
        with open("./settings.json", "w") as f:
            json.dump(data, f, ensure_ascii=True, indent=2)

        print("___File Updated Successfully___")

    def setCmdPass(self):
        inp_pwd = getpass(prompt="Enter Current Password: ", stream=None)
        inp_pwd = hashlib.md5(inp_pwd.encode()).hexdigest()

        old_pwd = self.getCmdPass()

        if inp_pwd == old_pwd:
            pwd = input("Enter New Pasword: ")
            pwd = hashlib.md5(pwd.encode()).hexdigest()
            self.settings["pass"] = pwd
            self.writeTofile(self.settings)
        else:
            print("Wrong Password !!!")

    def getCmdPass(self):
        if self.settings["pass"] != "":
            return self.settings["pass"]
        else:
            pwd = input("Set a password for app: ")
            pwd = hashlib.md5(pwd.encode()).hexdigest()
            self.settings["pass"] = pwd
            self.writeTofile(self.settings)
            return self.settings['pass']

    def setAlias(self):
        try:
            name = input("Enter Alias Name: ")
            value = input("Enter Alias Value: ")
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

    def removeAlias(self):
        try:
            self.getAliasList()
            name = input("Enter name of alias to remove: ")
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

        print()


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


def configure():
    print('\n')
    tprint("pswd\nManager", "larry3D-xlarge")
    print(f"[0] Set Alias")
    print(f"[1] Delete Alias")
    print(f"[2] Set Commandline Password")
    print()

    choice = int(input("> "))
    if choice == 0:
        Configure().setAlias()
    elif choice == 1:
        print("Available Aliases")
        Configure().removeAlias()
    elif choice == 2:
        Configure().setCmdPass()


if __name__ == "__main__":
    configure()
