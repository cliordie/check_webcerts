from email.mime.text import MIMEText
import smtplib

smtpServer = ''

def certNotification (expDays, serverNM, siteNM, CertEXP):
    subject = expDays + ' Day Certificate Expiration Notice | ' + siteNM
    sender = 'sender@email.com'
    receivers = ['example@email.com']
    
    text_subtype = 'html'

    msgBody = "<h2> The SSL Certficate for " + siteNM + " will expire in " + expDays + " days. </h2> Server Name: " + serverNM +  "</br>" + "Site Name: " + siteNM + "</br>" + "Expiration Date: " + CertEXP

    msg = MIMEText(msgBody, text_subtype)
    msg['Subject'] = subject
    msg['From'] = 'Certificate Monitor <' + sender + '>'
    msg['To'] = 'example@email.com'

    try:
        smtpObj = smtplib.SMTP(smtpServer)
        smtpObj.sendmail(sender, receivers, msg.as_string())         
        print ("Successfully sent email")
    except:
        print ("Error: Failed to send email")