# calendar_event.py - Class for sending calendar invitations
# -*- coding: utf-8 -*-
__version__ = '0.1'
__all__ = ['CalendarInvite']

import os
import sys
import datetime
from datetime import datetime as dt
from email.mime.multipart import MIMEMultipart
from email.mime.multipart import MIMEBase
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
from email.encoders import encode_base64
import smtplib


class HaltException(Exception): pass


class CalendarInvite():
    """ Class for sending calendar invitations via email. """

    def __init__(self):
        #self.data = {"Name": call['Name'], "Day": call['Weekday'], "Date": call['Date'], "Time": call['Time']} # @FIXME
        pass

    def send_invite(self, call) -> None:
        """ Given a dict with appropriate values, emails ics calendar invite. """
        CRLF = "\r\n"
        login = call['login']
        FROM = call['from']
        description = call['description']+CRLF
        attendees = call['attendees']
        organizer = call['organizer']

        try:
            confirmation = os.environ['CAL_KEY']
        except HaltException as ha:
            print("No authentication methods left to try.")

        #ddtstart = datetime.datetime.now()
        #dtoff = datetime.timedelta(days = 1)
        dur = datetime.timedelta(hours = 1)
        #ddtstart = ddtstart +dtoff
        ddtstart = call['datetime']
        ddtstart = ddtstart + datetime.timedelta(hours=5)
        dtend = ddtstart + dur
        dtstamp = datetime.datetime.now().strftime("%Y%m%dT%H%M%SZ")
        dtstart = ddtstart.strftime("%Y%m%dT%H%M%SZ")
        dtend = dtend.strftime("%Y%m%dT%H%M%SZ")

        description = description +CRLF
        attendee = ""
        for att in attendees:
            attendee += "ATTENDEE;CUTYPE=INDIVIDUAL;ROLE=REQ-    PARTICIPANT;PARTSTAT=ACCEPTED;RSVP=TRUE"+CRLF+" ;CN="+att+";X-NUM-GUESTS=0:"+CRLF+" mailto:"+att+CRLF
        ical = "BEGIN:VCALENDAR"+CRLF+"PRODID:pyICSParser"+CRLF+"VERSION:2.0"+CRLF+"CALSCALE:GREGORIAN"+CRLF
        ical+="METHOD:REQUEST"+CRLF+"BEGIN:VEVENT"+CRLF+"DTSTART:"+dtstart+CRLF+"DTEND:"+dtend+CRLF+"DTSTAMP:"+dtstamp+CRLF+organizer+CRLF
        ical+= "UID:FIXMEUID"+dtstamp+CRLF
        ical+= attendee+"CREATED:"+dtstamp+CRLF+description+"LAST-MODIFIED:"+dtstamp+CRLF+"LOCATION:"+CRLF+"SEQUENCE:0"+CRLF+"STATUS:CONFIRMED"+CRLF
        ical+= "SUMMARY:Call with Forest Mars: "+ddtstart.strftime("%b %d %Y @ %H:%M")+CRLF+"TRANSP:OPAQUE"+CRLF+"END:VEVENT"+CRLF+"END:VCALENDAR"+CRLF

        body_tmpl = open('assets/email/body.txt', 'r')
        #email_body = call['body']
        self.data = {"Name": call['who'], "Day": call['weekday'], "month_name": call['month_name'], "day": call['day'], "ord": call['ord'], "time_hour": call['hour'], "time_minutes": call['mins'], "ampm": call['ampm']} # @FIXME
        email_body = body_tmpl.read().format(**self.data)
        body_bin = "This is the email body in binary - two steps"

        msg = MIMEMultipart('mixed')
        msg['From'] = FROM
        msg['Reply-To']=FROM
        msg['To'] = ",".join(attendees)
        msg['Date'] = formatdate(localtime=True)
        msg['Subject'] = call['Subject']

        part_email = MIMEText(email_body, "html")
        part_cal = MIMEText(ical,'calendar;method=REQUEST')
        msgAlternative = MIMEMultipart('alternative')
        msg.attach(msgAlternative)
        ical_attach = MIMEBase('application/ics',' ;name="%s"'%("invite.ics"))
        ical_attach.set_payload(ical)
        encode_base64(ical_attach)
        ical_attach.add_header('Content-Disposition', 'attachment; filename="%s"'%("invite.ics"))
        email_attach = MIMEText('', 'text/html')
        encode_base64(email_attach)
        email_attach.add_header('Content-Transfer-Encoding', "")
        msgAlternative.attach(part_email)
        msgAlternative.attach(part_cal)

        mailServer = smtplib.SMTP('smtp.gmail.com', 587)
        mailServer.ehlo()
        mailServer.starttls()
        mailServer.ehlo()
        mailServer.login(login, confirmation)
        mailServer.sendmail(FROM, attendees, msg.as_string())
        mailServer.close()



if __name__ == '__main__':
    call = {}
    call['login'] = ''
    call['from'] = ''
    call['description'] = ''
    call['attendees'] = []
    call['organizer'] = []

    #cal_test = CalendarInvite()
    #cal_test.send_invite(call)


# Ca. https://www.w3.org/Protocols/rfc1341/7_2_Multipart.html
# https://developers.google.com/calendar/quickstart/python
