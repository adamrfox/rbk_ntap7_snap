#!/usr/bin/python

import getpass
import sys
from codecs import encode, getdecoder

user = {}
passwd = {}
i = -1
while True:
    i += 1
    if int(sys.version[0]) < 3:
        array = raw_input ("Enter Array type: (blank if done): ")
    else:
        array = input("Enter Array type (blank if done): ")
    if array == "":
        break
    if int(sys.version[0]) < 3:
        user[array] = raw_input("Enter User: ")
    else:
        user[array] = input("Enter User: ")
    passwd[array] = getpass.getpass("Enter Password: ")
fp = open(sys.argv[1], "w")
data = ""
for x in user.keys():
    ent_s = x + ":" + user[x] + ":" + passwd[x] + "\n"
    data = data + ent_s
if int(sys.version[0]) < 3:
    data = data.encode('rot13')
    data = data.encode('uu_codec')
    fp.write(data)
else:
    r13 = getdecoder('rot-13')
    data = r13(data)[0]
    data = encode(bytes(data, 'utf-8'), 'uu')
    data = str(data)[2:len(str(data))-3]
    data_s = str(data).split('\\n')
    for line in data_s:
        fp.write(line + '\n')
fp.close()
