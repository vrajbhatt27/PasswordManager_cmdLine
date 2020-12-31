import json
import sys
from sys import argv
from getpass import getpass

operation = None
param = None
data = None


def initial():
    global data, operation, param
    #  Opens a file and read data from it. If file is empty then it creates a new data dict
    try:
        f = open(
            r'C:/Users/91982/Desktop/Jarvis/Python/Python Projects/pwd manager/data.json')
        data = json.load(f)
        f.close()
    except:
        data = {}

    # f = open(
    #     r'C:/Users/91982/Desktop/Jarvis/Python/Python Projects/pwd manager/data.json')
    # data = json.load(f)
    # f.close()

    if len(argv) != 3:
        print("Less Arguments")
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
        with open(r'C:/Users/91982/Desktop/Jarvis/Python/Python Projects/pwd manager/data.json', 'w') as f:
            json.dump(data, f, ensure_ascii=True, indent=2)

        print("File Updated")
    except:
        print("!!! File Updation Failed !!!")


def getData(param):
    if param == '1':
        field = input("field: ")
        pwd = input("password: ")

        data[field] = pwd
    elif param == '2':
        domain = input("Enter Domain: ")
        fields = input("Enter all fields: ")
        fields = fields.split(' ')
        info = {}
        for i in fields:
            inp = input(i+": ")
            info[i] = inp

        data[domain] = info

    write2file()


def showData(param):
    fexists(param)
    if param != 'all':
        res = param

        if type(data[res]) == dict:
            for k, v in data[res].items():
                print(k, ": ", v)
        else:
            print(data[res])
    elif param == 'all':
        for k, v in data.items():
            if type(v) == dict:
                print("---{0}---".format(k))
                for f, d in v.items():
                    print("\t{0}: {1}".format(f, d))
            else:
                print("{0}: {1}".format(k, v))

            print()


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
        val[field] = value

        data[param] = val
    else:
        value = input("Enter value: ")
        data[param] = value

    write2file()
    # print(data)


def deleteData(param):
    fexists(param)
    data.pop(param)
    print(param, "Deleted Successfully")
    write2file()


verify = getpass(prompt="Password: ", stream=None)

if verify == '1423':
    initial()
    if operation == 'w':
        getData(param)
    elif operation == 'r':
        showData(param)
    elif operation == 'u':
        updateData(param)
    elif operation == 'd':
        deleteData(param)
else:
    print("!!! Wrong password !!!")
