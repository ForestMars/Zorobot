#!/usr/bin/env python
# -*- coding: utf-8 -*-
# app.py (smsbot) - SMS message dispatcher and handler. Don't get me started.
__version__ = '0.5.1'
CONDA_ENV = 'chatbot1'

import os
import csv
import json
import logging
import magic
import random
from random import choice
import shlex
import subprocess
import time

from flask import Flask, Response, request, redirect, session
from flask_session import Session
#import redis
import requests
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
from waitress import serve

#import contacts
from common.lumberjack import Log as log
from common.utils import ddict, HaltException as HX
from common import utils
from include.cv import VisionAPI

"""
def csv_to_dict(file):
    #mydict = {y[0]: y[1] for y in [x.split(",") for x in open(file).read().split('\n') if x]}
    with open(file) as f:
        d = dict(filter(None, csv.reader(f)))

    return d

def rev_dict(dict):
    inv_dict = {v: k for k, v in dict.items()}

    return inv_dict
"""

def validate_number(number):
    number = str(number).strip(' ').replace('+', '')

    if len(number) == 11 and number.startswith('1'):
        return number.replace('1', '', 1)
    elif len(number) == 10 and not number.startswith('1'):
        return number


def prefix_number(number):
    numba = str(number)

    if len(numba) == 10 and not numba.startswith('1'):
        return '+1' + numba
    elif len(numba) == 11 and numba.startswith('1'):
        return '+' + numba
    elif len(numba) == 12 and numba.startswith('+1'):
        return numba


def lookup_contact(numba):
    numba = validate_number(numba)

    # #TODO: cache w/ redis.
    peops = utils.csv_to_dict('assets/contacts.csv')
    lookup = utils.rev_dict(peops)

    if numba in lookup:
        who = lookup[numba].split()[0]
    else:
        who = numba

    return who


def rev_lookup(who):
    numba = None # 🙄

    # #TODO: cache w/ redis.
    peops = utils.csv_to_dict('assets/contacts.csv')

    # @TODO: store first and last so we can hash, not iterate.
    for peop in peops:
        if who.lower() == peop.split()[0].lower():
            numba = peops[peop]

    return numba


command = shlex.split("env -i bash -c 'source .env && env'")
proc = subprocess.Popen(command,
    stdout=subprocess.PIPE,
    encoding='utf8',
    universal_newlines=True
    )
for line in proc.stdout:
  (key, _, value) = line.partition("=")
  os.environ[key] = value.strip()
proc.communicate()

try:
    account_sid = os.environ['TW_ACCT_SID']
except HX as ha:
    print("Sorry, no SID found.")
try:
    auth_token = os.environ['TW_AUTH_TOKEN']
except HX as ha:
    print("Sorry, no authentication token found.")
try:
    client = Client(account_sid, auth_token)
except HX as ha:
    print("Um...")

if 'AZURE_SUB_KEY' in os.environ:
    sub_key = os.environ['AZURE_SUB_KEY']


HOST = '3.137.143.152'
DOMAIN = 'scheduler'
nassau='+15166982705'
upstate="+18458680258"
belvedere="+14157122019"


# back-to-front
app = Flask(__name__)
session_=Session()

#r = redis.StrictRedis(host=redis_host, port=redis_port, password=redis_password, decode_responses=True)
#r.set('counter', 1)


@app.route('/test')
def ifucancme():
    return '"If you can see me I can see you."'

@app.route('/xml')
def xmlTest(payload):
    xml = '<result>payload</result>'
    return Response(xml, mimetype='text/xml')

@app.route('/incall',methods = ['POST', 'GET'])
def incall():
    xml = "<Response><Say voice='alice'>Hi, this is Forest's A Eye assistant. Sorry he can't come to the phone, he's off doing some A Eye or something, I don't know he never tells me anything.</Say><Pause length='1'/><Say voice='alice'>But I'll tell him you called, and just between you and me, he'll be glad to hear that.</Say></Response>"
    return Response(xml, mimetype='text/xml')

@app.route('/sms',methods = ['GET', 'POST'])
def sms():
    msg = request.form.to_dict() # Not currently used, but cast as dict so we can add additional keys. (@FIXME: Shouldn't this be in handler?)
    msg['From'] = msg['From'].replace(' ','') # ('+' handling)

    if 'MediaUrl0' in msg:
        media = HandleMedia()
        media.media_files(msg)
        if msg['Body'].replace(' ', '') == '':
            return Response('resp', mimetype='text/xml')

    resp = handle_msg(msg)

    # @TODO: Needs refactoring.
    if isinstance(resp, str): # 🦆
        send_msg(msg['From'], resp)
        return Response(resp, mimetype='text/xml')
    else:
        try:
            replies = json.loads(resp.content.decode('UTF-8'))
        except Exception as e:
            print(e)
        try:
            if len(replies) > 0:
                for r in replies:
                    who = r['recipient_id']
                    reply = r['text']
                    try:
                        send_msg(who, reply)
                    except Exception as e:
                        print(e)
                        # log(e)  # init warning
        except TypeError:
            send_msg(who, "What can I say")

        return Response(resp, mimetype='text/xml')


class HandleMedia(object):
    def __init__(self):
        pass

    # @TODO: Refactor multiple file handling.
    def media_files(self, msg):
        for m in range(10):
            url = 'MediaUrl' + str(m)
            if url in msg:
                r = requests.get(msg[url])
                file = r.content
                with open('tmp', 'wb') as f:
                    f.write(r.content)
                now = str(int(time.time()))
                mimetype, filetype = self.get_mimetype('tmp')
                path = 'files/' + mimetype + '/'
                file = msg['From'].replace('+','') + '_' + now + '.' + filetype
                with open(path + file, 'wb') as f:
                    f.write(r.content)
                describe = "That looks like " + self.id_image(path + file)
                send_msg(msg['From'], describe)
            elif url not in msg:
                return

    def get_mimetype(self, file):
        log.debug("Scanning %s" % file)
        mimetype = utils.id_mime_type(file)
        mimetypes = ['image/jpeg', 'image/png']
        if any(mimetype in m for m in mimetypes): # python can b verbose
            if 'image' in mimetype:
                filetype = mimetype.replace('image/', '')
                return mimetype, filetype
            else:
                return 'other', 'xyz'

    def id_image(self, img):
        print('id fired')
        vision = VisionAPI(sub_key)
        descr = vision.analyse(img)
        print(descr)
        return descr.lower()

    def handle_res(file):
        """ Upload resume in pdf or docx format. """
        pass


def handle_cmd(msg):
    if msg['From'] == nassau:
        if msg['Body'].lower().startswith('to'):
            cmd = msg['Body'].lower().replace('to', '', 1).split()
            who_to = cmd.pop(0)
            say_what = ' '.join(cmd)
            numba = rev_lookup(who_to)
            to = prefix_number(numba)
            send_msg(to, say_what)

            return True


# @TODO: This should be a class & plainly needs refactoring.
def handle_msg(msg: dict) ->list:
    """ Handler for message request object. Logs message and returns list of responses."""
    if handle_cmd(msg) is not None:
        return

    msg_alert(msg['From'], msg['Body'])
    msg, lol = parse_msg(msg)

    if lol is not None:
        resp = lol
    elif lol is None:
        resp = get_response(msg)

    log_msg = [
        {'From': msg['From']},
        {'Message': msg['Body']},
        ]

    return(resp)


def parse_msg(msg):
    """ Handler mostly for people that prepend 'lol' to everything they say. """
    msg_ = msg
    if (msg_['Body'].lower().startswith('lol ') or msg_['Body'].lower() == 'lol'):
        msg_['Body'] = msg_['Body'].lower().replace('lol', '')
        if len(msg_['Body']) > 0:

            return msg_, None
        else:
            lolz = ["😂", "🤣", "Pretty funny, huh?", "I'm laughing so hard"]
            return msg_, choice(lolz)

    return msg, None


def get_response(msg, who='default'):
    url = 'http://' + HOST + ':5005/'
    txt = msg['Body']
    who = msg['From'] # NB. the leading '+' is simply ignored.
    ENDPOINT = url + 'conversations/' + who + '/respond'
    r = requests.get(ENDPOINT, params={'query': txt})

    return(r)


def send_msg(to, body):
    """ Send SMS reply via API """
    time.sleep(random.randrange(7, 11))
    who = lookup_contact(to)
    if who.lower() == 'block':
        return
    if who.lower() == 'blocked':
        return
    if who.lower() == 'null':
        return
    try:
        message = client.messages.create(to=to, from_=belvedere, body=body)
        #print(message.sid)
    except Exception as e:
        print(e)


    msg_cc(who, body) # (not always necessary.)


def msg_alert(numba, body):
    who = lookup_contact(numba)

    if prefix_number(who) != nassau:
        incoming = 'msg from ' + who + ': ' + body
        try:
            message = client.messages.create(to=nassau, from_=belvedere, body=incoming)
            #print(message.sid)
        except Exception as e:
            print(e)


def msg_cc(who, body):

    if prefix_number(who) != nassau:
        outgoing = 'msg to ' + who + ': ' + body

        try:
            message = client.messages.create(to=nassau, from_=belvedere, body=outgoing)
            print(message.sid)
        except Exception as e:
            print(e)


def get_port(domain=DOMAIN):
    """ Gets port number for the current active domain model """
    pass


def who_this(): #placeholder
    pass


# @TODOs
# if response == 'bye': reset connection (after storing meeting deets)


if __name__ == "__main__":
    app.secret_key = 'SECRET' # If I told you, it wouldn't be.
    #session_.init_app(app)
    #app.config['SESSION_TYPE'] = 'filesystem'
    #app.run(host='0.0.0.0', port= 80, debug=False)
    #app.run(host='0.0.0.0', port= 5531, debug=True)
    serve(app, host='0.0.0.0', port=5531)
