from gettext import find
from http import server
import ssl
import datetime
import socket
import ipaddress
from time import timezone
import psycopg2
from infoblox import getNetworks
import db

## Insert Line into OpsView DB
def newCertline(serverNM,serverIP,certIssuedTo,certIssuedBy,certExpiration):
    currentDate = datetime.date.today()

    conn = psycopg2.connect (
        dbname = db.psdbname,
        host = db.psdbserver,
        user = db.psdbuser,
        password = db.psdbpass,
        sslmode = db.dbsslmode
        
    )
    dbresult = None
    dbinsert = '''INSERT INTO ops_certificates (server_nm, server_ip, cert_issued_to, cert_issued_by, cert_expiration, data_date) Values (%s, %s, %s, %s, %s, %s)'''
    dbupdate = '''UPDATE ops_certificates SET (server_nm, server_ip, cert_issued_to, cert_issued_by, cert_expiration, data_date) = (%s, %s, %s, %s, %s, %s) WHERE server_ip = %s'''
    dbcheck = "SELECT * from ops_certificates WHERE server_ip = %s"
    
    cur = conn.cursor()
    cur.execute(dbcheck, (serverIP,))
    try :
        dbresult = cur.fetchone
    except :
        dbresult = None
    
    if dbresult == None:

        print(serverIP + 'Does not exist in table. Adding')
        cur.execute(dbinsert, (serverNM,serverIP,certIssuedTo,certIssuedBy,certExpiration,currentDate))
        conn.commit()
        cur.close()
        
    else:

        print(serverIP + " exists in table. Updating with new Information")
        cur.execute(dbupdate, (serverNM,serverIP,certIssuedTo,certIssuedBy,certExpiration,currentDate,serverIP))
        conn.commit()
        cur.close()


## Get Certificate Data
def get_certificate(passipaddr, hostname, port):
    err = 0
    peername = None
    cert = None
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_REQUIRED
    with ctx.wrap_socket(socket.socket(), server_hostname=hostname) as sock_ssl:
        sock_ssl.settimeout(2)
        try:
            sock_ssl.connect((hostname,port))
            cert = sock_ssl.getpeercert()
        except:
            print ("Failed to establish a connection on port 443")
            err = 1

    if err == 0:
        subject = dict(x[0] for x in cert['subject'])
        issued_to = subject['commonName']
        issuer = dict(x[0] for x in cert['issuer'])
        issued_by = issuer['commonName']

        certExpDate = datetime.datetime.strptime(cert['notAfter'], '%b %d %H:%M:%S %Y %Z')
        certExpires = (certExpDate - datetime.datetime.now())

        print ("Address          : https://" + hostname)
        print ("Issued To        :",issued_to)
        print ("Issued By        :",issued_by)
        print ("Expiration Date  :",certExpDate)
        print ("Expires in      :",certExpires)

        sock_ssl.close()

        newCertline(serverNM=hostname, serverIP=passipaddr, certIssuedTo=issued_to, certIssuedBy=issued_by, certExpiration=certExpDate)

## Iterate through all IP Ranges pulled from Infoblox"
for network in getNetworks():
    print ("Network : " + network)
    for ip in ipaddress.IPv4Network(network):
        print ("-----------------------------")
        ipaddr = str(ip)
        err = 0
        siteaddr = None
        hostname = None
        try :
            siteaddr=socket.gethostbyaddr(ipaddr)
            hostname=siteaddr[0]
        except:
            print (ipaddr + " : Does not resolve")
            err = 1
        
        if err == 0:
            print(ipaddr + " : " + hostname)
            get_certificate (passipaddr=ipaddr,hostname=hostname,port=443)
        
