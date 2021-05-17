import json
import os
import sys
from sys import argv
from getpass import getpass
import config
import pyperclip as clip


operation = None
param = None
data = None
toBeCopied = False


def initial():
    global data, operation, param
    #  Opens a file and read data from it. If file is empty then it creates a new data dict

    try:
        f = open(
            r'./data.json')
        data = json.load(f)
        f.close()
    except:
        data = {}

    if('list' in argv):
        operation = argv[1]
    else:
        if len(argv) != 3:
            print("Less Arguments")
            sys.exit(0)
        else:
            operation = argv[1]
            param = argv[2]

def fexists(param):
    if (param not in data.keys()) and (param != 'all'):
        print("!!! Not present in file !!!")
        sys.exit(0)

def write2file():
    # writes data to file
    try:
        with open(r'./data.json', 'w') as f:
            json.dump(data, f, ensure_ascii=True, indent=2)

        print("File Updated")
    except:
        print("!!! File Updation Failed !!!")

def getData(param):
    if param == '1':
        field = input("Enter field: ")
        pwd = input("Enter password: ")
        pwd = config.encrypt_json(pwd)

        data[field] = pwd
    elif param == '2':
        domain = input("Enter Domain: ")
        fields = input("Enter all fields: ")
        fields = fields.split(' ')
        info = {}
        for i in fields:
            inp = input(i+": ")
            inp = config.encrypt_json(inp)
            info[i] = inp

        data[domain] = info

    write2file()


def showData(param):
    fexists(param)
    if param != 'all':
        res = param

        if toBeCopied:
            if type(data[res]) == dict:
                for k, v in data[res].items():
                    v = config.decrypt_json(v)
                    if(k == 'pwd'):
                        clip.copy(v)
                        print("Password Copied for {0}".format(param))
            else:
                clip.copy(config.decrypt_json(data[res]))
                print("Password Copied for {0}".format(param))
        else:
            if type(data[res]) == dict:
                for k, v in data[res].items():
                    v = config.decrypt_json(v)
                    print(k, ": ", v)
            else:
                print(config.decrypt_json(data[res]))

    elif param == 'all' and toBeCopied == False:
        for k, v in data.items():
            if type(v) == dict:
                print("---{0}---".format(k))
                for f, d in v.items():
                    print("\t{0}: {1}".format(f, config.decrypt_json(d)))
            else:
                print("{0}: {1}".format(k, config.decrypt_json(v)))

            print()
    elif param == 'all' and toBeCopied == True:
        print("!!! Can't Copy !!!")


def updateData(param):
    fexists(param)
    val = data[param]
    if type(val) == dict:
        print("What do u want to update? : ", end=' ')
        for k in val.keys():
            print("[{0}]".format(k), end=' ')

        print()

        field = input("Enter field: ")
        value = input("Enter Value: ")
        value = config.encrypt_json(value)
        val[field] = value

        data[param] = val
    else:
        value = input("Enter value: ")
        value = config.encrypt_json(value)
        data[param] = value

    write2file()


def deleteData(param):
    fexists(param)
    data.pop(param)
    print(param, "Deleted Successfully")
    write2file()

def getFromAlias(param):
    param = config.Alias().getAliasValue(param)
    if param != None:
        showData(param)

def getList():
    map = {}
    for ind, i in enumerate(list(data.keys())):
        map[ind] = i

    for k,v in map.items():
        print(f"[{k}] {v}")
    print("\n")
    choice = int(input('>'))
    res = map[choice]
    if type(data[res]) == dict:
        for k, v in data[res].items():
            v = config.decrypt_json(v)
            print(k, ": ", v)
    else:
        print(config.decrypt_json(data[res]))

verify = getpass(prompt="Password: ", stream=None)

if verify == '1423':
    initial()
    if operation == 'w':
        getData(param)
    elif operation == 'r':
        showData(param)
    elif operation == 'rc':
        toBeCopied = True
        showData(param)
    elif operation == 'u':
        updateData(param)
    elif operation == 'd':
        deleteData(param)
    elif operation == 'list':
        getList()
    elif operation == 'a':
        getFromAlias(param)
    elif operation == 'set':
        name = input("Enter Alias Name: ")
        value = input("Enter Alias Value: ")
        config.Alias().setAlias(name, value)
    elif operation == 'del':
        config.Alias().removeAlias(param)
    elif operation == 'alias':
        config.Alias().getAliasList()

else:
    print("!!! Wrong password !!!")
