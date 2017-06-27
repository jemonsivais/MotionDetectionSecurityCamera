import smtplib
import datetime
import email
import email.mime.application
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.MIMEBase import MIMEBase
from email import Encoders

def sendEmail(addr, passwd, server):
    ##Construct message
    msg = MIMEMultipart()
    msg['From']=addr
    msg['To']=addr
    msg['Subject']="Motion was detected in your room!"
    body = "There was motion detected in your room on "+datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p")
    msg.attach(MIMEText(body,'plain'))

    ##Attach email
    filename = 'feed.avi'
    fo = open(filename,"rb")
    att = email.mime.application.MIMEApplication(fo.read(),_subtype="avi")
    fo.close()
    att.add_header('Content-Disposition', 'attachment', filename=filename)
    msg.attach(att)

    ##Send email
    server = smtplib.SMTP(server, 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(addr, passwd)
    text = msg.as_string()
    server.sendmail(addr, addr, text)
    
