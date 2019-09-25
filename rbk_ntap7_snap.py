#!/usr/bin/python

from __future__ import print_function
import sys
import getopt
import getpass
import time
sys.path.append('./NetApp')
from NaServer import *


def usage():
    sys.stderr.write("Usage: rbk_ntap7_snap.py [-h] [-c creds] [-v] [-n name] ntap create|delete volume\n")
    sys.stderr.write("-h | --help : Prints this message\n")
    sys.stderr.write("-c | --creds= : Specify the credentials on the command line user:password or creds file\n")
    sys.stderr.write("-v | --verbose : Verbose Mode.  Prints more steps\n")
    sys.stderr.write("-n | --name= : Set name of the snapshot (rubrik by default)\n")
    sys.stderr.write("ntap : Name or IP of the NetApp\n")
    sys.stderr.write("create|delete : keyword to create or delete the snapshot\n")
    sys.stderr.write("volume : The volume of the snapshot\n")
    exit (0)

# SDK Error checking functions
def ntap_set_err_check(out):
    if(out and (out.results_errno() != 0)) :
        r = out.results_reason()
        print("Connection to filer failed" + r + "\n")
        sys.exit(2)

def ntap_invoke_err_check(out):
    if(out.results_status() == "failed"):
            print(out.results_reason() + "\n")
            sys.exit(2)

# Grabs teh credentials from a file.  Uses type 'ntap'
def get_creds_from_file (file):
    with open(file) as fp:
        data = fp.read()
    fp.close()
    data = data.decode('uu_codec')
    data = data.decode('rot13')
    lines = data.splitlines()
    for x in lines:
        if x == "":
            continue
        xs = x.split(':')
        if xs[0] == "ntap":
            ntap_user = xs[1]
            ntap_password = xs[2]
    return (ntap_user, ntap_password)

# SDK call to delete the snapshot.
def ntap_delete_snap(netapp, volume, name):
    ntap_snap = NaElement('snapshot-delete')
    ntap_snap.child_add_string("volume", volume)
    ntap_snap.child_add_string("snapshot", name)
    results = netapp.invoke_elem(ntap_snap)
    ntap_invoke_err_check(results)
    vprint("Deleted snaphot " + name + " on volume " + volume)
    return()

# Verbose print
def vprint(message):
    if verbose:
        print (message)
    return()

if __name__ == '__main__':

    verbose = False
    ntap_user = ""
    ntap_password = ""
    creds_file = ""
    snap_name = "rubrik"

# Parse arguments
    optlist, args = getopt.getopt(sys.argv[1:], 'hc:vn:', ['--help', '--creds=', '--verbose', '--name='])
    for opt, a in optlist:
        if opt in ('-h', '--help'):
            usage()
        if opt in ('-c', '--creds'):
            creds_file = a
        if opt in ('-v', '--verbose'):
            verbose = True
        if opt in ('-n', '--name'):
            snap_name = a

    if args[0] == "?":
        usage()
    (ntap_addr, function, volume) = args
# Get NTAP creds
    if creds_file != "":
        (ntap_user, ntap_password) = get_creds_from_file(creds_file)
    if ntap_user == "":
        if int(sys.version[0]) < 3:
            ntap_user = raw_input("NTAP User: ")
        else:
            ntap_user = input("NTAP User: ")
    if ntap_password == "":
        ntap_password = getpass.getpass("NTAP Password: ")

# Set up NetApp SDK
    netapp = NaServer(ntap_addr, 1, 15)
    out = netapp.set_transport_type('HTTP')
    ntap_set_err_check(out)
    out = netapp.set_style('LOGIN')
    ntap_set_err_check(out)
    out = netapp.set_timeout(30)
    ntap_set_err_check(out)
    out = netapp.set_admin_user(ntap_user, ntap_password)
    ntap_set_err_check(out)

# Snap create process.  If snap exists, delete it first
    if function == "create":
        snap_api = NaElement('snapshot-list-info')
        snap_api.child_add_string('volume', volume)
        results = netapp.invoke_elem(snap_api)
        ntap_invoke_err_check(results)
        snap_info = results.child_get('snapshots').children_get()
        for s in snap_info:
            name = s.child_get_string("name")
            if name == snap_name:
                ntap_delete_snap(netapp, volume, snap_name)
        ntap_snap = NaElement('snapshot-create')
        ntap_snap.child_add_string("volume", volume)
        ntap_snap.child_add_string("snapshot", snap_name)
        results = netapp.invoke_elem(ntap_snap)
        ntap_invoke_err_check(results)
        vprint ("Created snapshot " + snap_name + " on volume " + volume)

# Snap delete process.  Simply calls the function
    elif function == "delete":
        ntap_delete_snap(netapp, volume, snap_name)


