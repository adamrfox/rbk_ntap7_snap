#!/usr/bin/python

from codecs import encode
import getpass
import sys


user = {}
passwd = {}
i = -1
while True:
    i += 1
    if int(sys.version[0]) < 3:
        array = raw_input ("Enter Array type: (blank if done): ")
    else:
        array = input("Enter Array type: (blank if done): ")
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
    data = encode(data, 'rot13')
    data = str.encode(data)
    data = encode(data, 'uu')
    data = str(data)
    data = data.replace("b'", "")
    lines = data.split("\\n")
    for l in lines:
        fp.write (l + "\n")
fp.close()
