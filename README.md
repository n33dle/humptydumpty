# humptydumpty

_Work in progress_

With administrative credentials, this tool will dump the lsass.exe proccess on a remote computer, download the dump file locally, which can then be processed through mimikatz on your local machine. The idea here is to obtain additional credentials from a compromised box, without the need of having to bypass AV.

In my testing, some AV will flag the dumping of the lsass process, however, in most cases the dumpfile will remain on the remote file system for a few seconds - enough to retrieve it as part of this script.

## Installation:
`pip3 install -r requirements`

## How to use:
*Single target:* `python3 humptydumpty.py -t <hostname/IP> -u <username> -p <password>`
*List of IPs/Hostnames from a file:* `python3 humptydumpty.py -f <filename> -u <username> -p <password>`

By default:
* Dumpfiles will be stored in current working directory, use -o to output to a different directory
* Local authentication is used, use -d to use domain authentication.
