# humptydumpty

With administrative credentials, this can be used to dump the lsass.exe proccess on a remote computer and download the dump file locally, which can then be processed through mimikatz.
In my testing, some AV will flag the dumping of the lsass process, however, in most cases the dumpfile will remain on the remote file system for a few seconds - enough to retrieve it as part of this script.

## Installation:
`pip install -r requirements`

## How to use:
`python3 humptydumpty.py -t <hostname/IP> -u <username> -p <password>`
