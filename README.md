# humptydumpty

With administrative credentials, this can be used to dump the lsass.exe proccess on a remote computer and download the dump file locally, which can then be processed through mimikatz.

## Installation:
`pip install -r requirements`

## How to use:
`python3 humptydumpty.py -t <hostname/IP> -u <username> -p <password>`
