#!/usr/bin/python

import getpass
import sys


user = {}
passwd = {}
i = -1
while True:
    i += 1
    array = raw_input ("Enter Array type: (blank if done): ")
    if array == "":
        break
    user[array] = raw_input("Enter User: ")
    passwd[array] = getpass.getpass("Enter Password: ")
fp = open(sys.argv[1], "w")
data = ""
for x in user.keys():
    ent_s = x + ":" + user[x] + ":" + passwd[x] + "\n"
    data = data + ent_s
data = data.encode('rot13')
data = data.encode('uu_codec')
fp.write (data)
fp.close()
