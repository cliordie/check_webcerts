from pickle import FALSE
import requests
from requests.auth import HTTPBasicAuth
import json
import appauth

def getNetworks():
    
    infobloxFQDN = 'scdhcp.chp.clarian.org'
    infobloxUser = appauth.getifbuser()
    infobloxPass = appauth.getifbSecret()

    print("Connecting to ", infobloxFQDN)
    networklist = None
    networklist = []
    requests.Session.verify = False
    response = None
    basicAuth = HTTPBasicAuth(infobloxUser, infobloxPass)
    r = requests.get("https://" + infobloxFQDN + "/wapi/v2.9/network?_max_results=10000", auth=basicAuth, verify=False)
    networkdata = json.loads(r.text)
    for networks in networkdata:
        network = networks['network']
        #print(network)
        networklist.append(network)
        
    networkcount = len(networklist)
    print("Networks Found: ",networkcount)  
    return(networklist)

