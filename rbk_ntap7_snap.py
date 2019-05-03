#!/usr/bin/python

import sys
import getopt
import getpass
import time
sys.path.append('./NetApp')
from NaServer import *


def usage():
    print "Usage goes here!"
    exit (0)

def ntap_set_err_check(out):
    if(out and (out.results_errno() != 0)) :
        r = out.results_reason()
        print("Connection to filer failed" + r + "\n")
        sys.exit(2)

def ntap_invoke_err_check(out):
    if(out.results_status() == "failed"):
            print(out.results_reason() + "\n")
            sys.exit(2)

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

def ntap_delete_snap(netapp, volume, name):
    print "Invoked delete!"
    ntap_snap = NaElement('snapshot-delete')
    ntap_snap.child_add_string("volume", volume)
    ntap_snap.child_add_string("snapshot", name)
    results = netapp.invoke_elem(ntap_snap)
    ntap_invoke_err_check(results)
    vprint("Deleted snaphot " + name + " on volume " + volume)
    return()

def vprint(message):
    if verbose:
        print message
    return()

if __name__ == '__main__':

    verbose = False
    ntap_user = ""
    ntap_password = ""
    creds_file = ""
    snap_name = "rubrik"

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

    (ntap_addr, function, volume) = args

    if creds_file != "":
        (ntap_user, ntap_password) = get_creds_from_file(creds_file)
    if ntap_user == "":
        ntap_user = raw_input("NTAP User: ")
    if ntap_password == "":
        ntap_password = getpass.getpass("NTAP Password: ")
    netapp = NaServer(ntap_addr, 1, 15)
    out = netapp.set_transport_type('HTTP')
    ntap_set_err_check(out)
    out = netapp.set_style('LOGIN')
    ntap_set_err_check(out)
    out = netapp.set_timeout(30)
    ntap_set_err_check(out)
    out = netapp.set_admin_user(ntap_user, ntap_password)
    ntap_set_err_check(out)
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
        print "invoking create " + snap_name
        results = netapp.invoke_elem(ntap_snap)
        print "Back from invoke"
        ntap_invoke_err_check(results)
        vprint ("Created snapshot " + snap_name + " on volume " + volume)
    elif function == "delete":
        ntap_delete_snap(netapp, volume, snap_name)


