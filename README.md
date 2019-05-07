# rbk_ntap7_snap
A project to integrate NTAP 7-mode snapshots and Rubrik

The idea here is to automate creating and deleting of NetApp snapshots.  As NTAP 7-mode is deprecated by NetApp,
no API integration for 7-mode ONTAP in Rubrik.  For those who wish to get similar snapshot functionality, this could be 
an option.

The script can create or delete a manual snapshot on a NetApp.  When creating a snapshot, if the snapshot exists, it
delete that snapshot and recreate it, essentially, refreshing it.  By default, the script names the snapshot 'rubrik'
but that can be changed on the command line.  

This script can be used along with the <a href="https://github.com/adamrfox/rbk_nas_backup"> pre/post script</a> I 
wrote if you like, or on its own.


