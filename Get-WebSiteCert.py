from urllib.request import Request, urlopen, ssl, socket
from urllib.error import URLError, HTTPError
from datetime import datetime
import json

#Do Not Use any Prefix
sitename = 'transfer.iuhealth.org'
port = '443'
siteaddress = (sitename, port)

sslinfo = ssl.get_server_certificate(siteaddress)
print(sslinfo)
