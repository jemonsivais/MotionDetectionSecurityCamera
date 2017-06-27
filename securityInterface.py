import sys
sys.path.append('/usr/local/lib/python2.7/dist-packages')
import motion
import thread
from pick import pick
address = ""
server = ""
passwd = ""

def setUp():
    address = raw_input('Enter your email address\n')
    title = 'Enter your email server'
    serverOptions = ['gmail','outlook', 'yahoo']
    (server, _) = pick(serverOptions, title, '=>')
    passwd = raw_input ('Enter your password\n')

    if(server == 'gmail'):
        server = 'smtp.gmail.com'
    if(server == 'outlook'):
        server = 'smtp.live.com'
    if (server == 'yahoo'):
        server = 'smtp.mail.yahoo.com'

def arm():
    thread.start_new_thread(motion.start, (address,passwd,server))

def disarm():
    thread.start_new_thread(motion.stop)
    
