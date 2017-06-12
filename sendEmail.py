import smtplib
import datetime
import email
import email.mime.application
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.MIMEBase import MIMEBase
from email import Encoders

def sendEmail():
    fromaddr = "fromaddr"
    toaddr = "toaddr"

    msg = MIMEMultipart()
    msg['From']=fromaddr
    msg['To']=toaddr
    msg['Subject']="Motion was detected in your room!"
    body = "There was motion detected in your room on "+datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p")
    msg.attach(MIMEText(body,'plain'))

    filename = 'feed.avi'
    fo = open(filename,"rb")
    att = email.mime.application.MIMEApplication(fo.read(),_subtype="avi")
    fo.close()
    att.add_header('Content-Disposition', 'attachment', filename=filename)
    msg.attach(att)
    
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(fromaddr, 'pass')
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    
