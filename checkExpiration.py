from datetime import datetime,timedelta
import psycopg2
import db
from notifications import certNotification

dateToday = datetime.now()

pgconn = psycopg2.connect (
        dbname = db.psdbname,
        host = db.psdbserver,
        user = db.psdbuser,
        password = db.psdbpass,
        sslmode = db.dbsslmode
    )

certQuery = 'SELECT * FROM ops_certificates'
certResult = None

cur = pgconn.cursor()
cur.execute(certQuery)
certResult = cur.fetchall()

for row in certResult:
    
    print("------------------------------")

    certServerNM = row[0]
    certSiteNM = row[2]
    certExpDate = row[4]
    
    print ("Server Name: ", certServerNM)
    print ("  Site Name: ", certSiteNM)
    print (" Expiration: ", certExpDate)
    
    strCertDate = datetime.strftime(certExpDate,"%y%m%d")
    certDate = datetime.strptime(strCertDate,'%y%m%d')
    noticeDate = str(certDate)

    strCurrentDate = dateToday.strftime("%y%m%d")
    currentDate = datetime.strptime(strCurrentDate,"%y%m%d")
    notice1Date = currentDate + timedelta(days=30)
    notice2Date = currentDate + timedelta(days=14)
    

    if certDate == notice1Date :
        certNotification(expDays='30',serverNM=certServerNM,siteNM=certSiteNM,CertEXP=noticeDate)
        print("30 Day Notification sent for " + certServerNM)

    if certDate == notice2Date :
        certNotification(expDays='14',serverNM=certServerNM,siteNM=certSiteNM,CertEXP=noticeDate)
        print("14 Day Notification sent for " + certServerNM)