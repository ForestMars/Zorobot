# calendar_event.py - Class for sending email with attachment
# -*- coding: utf-8 -*-
__version__ = '0.1'
__all__ = ['CalendarInvite']

import os
import sys
import datetime
from datetime import datetime as dt
from email.mime.multipart import MIMEMultipart
#from email.mime.multipart import MIMEMultipart
from email.mime.multipart import MIMEBase
from email.mime.text import MIMEText
#from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
#from email.utils import COMMASPACE, formatdate
from email.encoders import encode_base64
import smtplib

from os.path import basename
from email.mime.application import MIMEApplication

# check this
# from email.mime.base import MIMEBase
from email import encoders


#send_from = "forest@fractalgradient.com"
send_from = 'themarsgroup@gmail.com'
fromaddr = 'themarsgroup@gmail.com'
subject = "Resumé"


class HaltException(Exception): pass


# When you care enough to send the very best.
class Send():
    """ Class for sending something to someone. """

    def __init__(self):
        #self.data = {"Name": sendres['Name'], "email": sendres['email'], "res": sendres['res'], "kind": sendres['kind']} # @FIXME
        pass

    def send_mail(send_from, send_to, subject, text, files=None, server="127.0.0.1"):
        """ Given a working email server, sends email with attachment. Defaults to localhost. """
        assert isinstance(send_to, list)

        msg = MIMEMultipart()
        msg['From'] = send_from
        msg['To'] = COMMASPACE.join(send_to)
        msg['Date'] = formatdate(localtime=True)
        msg['Subject'] = subject

        msg.attach(MIMEText(text))

        for f in files or []:
            with open(f, "rb") as fil:
                part = MIMEApplication(
                    fil.read(),
                    Name=basename(f)
                )
            # After the file is closed
            part['Content-Disposition'] = 'attachment; filename="%s"' % basename(f)
            msg.attach(part)

        smtp = smtplib.SMTP(server)
        smtp.sendmail(send_from, send_to, msg.as_string())
        smtp.close()

    def send_email(self, sendres):

        msg = MIMEMultipart()

        msg['From'] = sendres['From']
        msg['To'] = sendres['To']
        msg['Subject'] = sendres['Subject']
        msg['Date'] = formatdate(localtime=True)

        #body = "ok then"
        body_tmpl = open('assets/email/send_something_body.txt', 'r')
        self.data = {"Name": sendres['Name']}
        body = body_tmpl.read().format(**self.data)

        msg.attach(MIMEText(body, 'html'))

        filename = "Forest\ Mars\ resume.pdf"
        attachment = open("assets/res/fm", "rb")

        part = MIMEBase('application', 'octet-stream')
        part.set_payload((attachment).read())
        encode_base64(part)
        part.add_header('Content-Disposition', "attachment; filename=%s" % filename)

        msg.attach(part)

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(fromaddr, os.environ['CAL_KEY'])
        text = msg.as_string()
        server.sendmail(msg['From'], msg['To'], text)
        #server.sendmail(fromaddr, toaddr, text)
        server.quit()



if __name__ == '__main__':
    #cal_test = CalendarInvite()
    #cal_test.send_invite(call)
    sendres = {}
    sendres['Name'] = "Name"
    sendres['From'] = "themarsgroup@gmail.com"
    sendres['To'] = "lostjournals@gmail.com"
    sendres['Subject'] = "Name Resume"
    sender = Send()
    try:
        sender.send_email(sendres)
    except Exception as e:
        print("oopsie, ", e)


# Ca. https://www.w3.org/Protocols/rfc1341/7_2_Multipart.html
# https://developers.google.com/calendar/quickstart/python
