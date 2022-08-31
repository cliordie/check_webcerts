from email.mime.text import MIMEText
import smtplib

smtpServer = 'smtp1.iuhealth.org'

def certNotification (expDays, serverNM, siteNM, CertEXP):
    subject = expDays + ' Day Certificate Expiration Notice | ' + siteNM
    sender = 'certmon@iuhealth.org'
    receivers = ['dcops@iuhealth.org']
    
    text_subtype = 'html'

    msgBody = "<h2> The SSL Certficate for " + siteNM + " will expire in " + expDays + " days. </h2> Server Name: " + serverNM +  "</br>" + "Site Name: " + siteNM + "</br>" + "Expiration Date: " + CertEXP

    msg = MIMEText(msgBody, text_subtype)
    msg['Subject'] = subject
    msg['From'] = 'IUH Certificate Monitor <' + sender + '>'
    msg['To'] = 'tjhewitt@iuhealth.org'

    try:
        smtpObj = smtplib.SMTP(smtpServer)
        smtpObj.sendmail(sender, receivers, msg.as_string())         
        print ("Successfully sent email")
    except:
        print ("Error: Failed to send email")