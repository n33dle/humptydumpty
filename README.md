# humptydumpty

With administrative credentials, this can be used to dump the lsass.exe proccess on any computer and download the dump file locally, which can then be processed through mimikatz to dump creds.

Pre-reqs:
pip3 install -r requirements

To run:
python3 humptydumpty.py -u <username> -p <password>
