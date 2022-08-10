import ssl
import datetime
import socket
from ranges import ipranges
import ipaddress
import psycopg2

## PostgreSQL Variables
psdbname = ''
psdbserver = ''
psdbuser = ''
psdbpass = ''

## Insert Line into OpsView DB
def newCertline(serverNM,serverIP,certIssuedTo,certIssuedBy,certExpiration):
    currentDate = datetime.date.today()

    conn = psycopg2.connect (
        dbname = psdbname,
        host = psdbserver,
        user = psdbuser,
        password = psdbpass 
    )
    dbinsert = '''INSERT INTO certificates (server_nm, server_ip, cert_issued_to, cert_issued_by, cert_expiration, data_date) Values (%s, %s, %s, %s, %s, %s)'''
    cur = conn.cursor()
    cur.execute(dbinsert, (serverNM,serverIP,certIssuedTo,certIssuedBy,certExpiration,currentDate))
    conn.commit()
    cur.close()

## Get Certificate Data
def get_certificate(passipaddr, hostname, port):
    err = 0
    peername = None
    cert = None
    ctx = ssl.create_default_context()
    with ctx.wrap_socket(socket.socket(), server_hostname=hostname) as sock_ssl:
        sock_ssl.settimeout(2)
        try:        
            sock_ssl.connect((hostname,port))
            peername = sock_ssl.getpeername()
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

## Iterate through all IP Ranges in "Ranges.py"
for range in ipranges:
    for ip in ipaddress.IPv4Network(range):
        print ("-----------------------------")
        print ("Checking ", ip)
        ipaddr = str(ip)
        #print ("Attempting to resolve hostname")
        err = 0
        siteaddr=None
        hostname = None
        try :
            siteaddr=socket.gethostbyaddr(ipaddr)
            hostname=siteaddr[0]
        except:
            print ("Does not resolve")
            err = 1
        
        if err == 0:
            #print ("hostname   :",hostname)
            #print ("IP Address :",ip)
            get_certificate (passipaddr=ipaddr,hostname=hostname,port=443)
        
