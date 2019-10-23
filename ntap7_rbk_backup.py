#!/usr/bin/python
import subprocess
import sys

def usage():
    sys.stderr.write("Usage: rbk_ntap7_backup.py ntap volume share rubrik\n")
    exit(0)

BASE_DIR = "/home/adamfox/demo"
RBK_BKP = BASE_DIR + "/rbk_nas_backup"
NTAP7_SNAP = BASE_DIR + "/rbk_ntap7_snap"
CREDS_FILE = NTAP7_SNAP + "/demo_creds"

try:
    (ntap, volume, share, fileset, rubrik) = sys.argv[1:]
except ValueError:
    usage()
cmd = RBK_BKP + "/rbk_nas_backup.py -c " + CREDS_FILE + " -P '" + NTAP7_SNAP + "/rbk_ntap7_snap.py -c " + CREDS_FILE + " " + ntap + " create " + volume + "' -p '" + NTAP7_SNAP + "/rbk_ntap7_snap.py -c " + CREDS_FILE + " " + ntap + " delete " + volume + "' -b " + ntap + ":" + share + " -f " + fileset + " " + rubrik
# print cmd
subprocess.call(cmd, shell=True)
