#!/usr/bin/env python
# -*- coding: utf-8 -*-
# app.py (smsbot) - SMS message dispatcher and handler. Don't get me started.
__version__ = '0.3'
CONDA_ENV = 'chatbot1'

import json
import os
import shlex
import subprocess
from random import choice

from flask import Flask, Response, request, redirect, session
from flask_session import Session
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
#import redis
import requests

#import contacts
from common.utils import HaltException as HX

#r = redis.StrictRedis(host=redis_host, port=redis_port, password=redis_password, decode_responses=True)
#r.set('counter', 1)

command = shlex.split("env -i bash -c 'source env/env.sh && env'")
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


HOST = '3.137.143.152'
DOMAIN = 'scheduler'
nassau='+15166982705'
upstate="+18458680258"
belvedere="+14157122019"


# back-to-front
app = Flask(__name__)
session_=Session()


@app.route('/test')
def helloIndex():
    return 'If you can see this...'

@app.route('/xml')
def xmlTest():
    xml = '<result>xml</result>'
    return Response(xml, mimetype='text/xml')

@app.route('/incall',methods = ['POST', 'GET'])
def incall():
    xml = "<Response><Say voice='alice'>Hi, this is Forest's A Eye assistant. Sorry he can't come to the phone, he's off doing some A Eye or something, I don't know he never tells me anything.</Say><Pause length='1'/><Say voice='alice'>But I'll tell him you called, and just between you and me, he'll be glad to hear that.</Say></Response>"
    return Response(xml, mimetype='text/xml')

@app.route('/sms',methods = ['GET', 'POST'])
def sms():
    msg = request.form.to_dict() # Not currently used, but cast as dict so we can add additional keys. (@FIXME: Shouldn't this be in handler?)
    msg['From'] = msg['From'].replace(' ','') # ('+' handling)
    resp = handle_msg(msg)

    # @TODO: Needs refactoring.
    if isinstance(resp, str): # 🦆
        send_msg(msg['From'], resp)
        return Response(resp, mimetype='text/xml')
    else:
        replies = json.loads(resp.content.decode('UTF-8'))
    if len(replies) > 0:
        for r in replies:
            print(r)
            who = r['recipient_id']
            reply = r['text']
            try:
                send_msg(who, reply)
            except Exception as e:
                print(e)

    return Response(resp, mimetype='text/xml')


# @TODO: This should be a class & plainly needs refactoring.
def handle_msg(msg: dict) ->list:
    """ Handler for message request object. Logs message and returns list of responses."""
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
    try:
        message = client.messages.create(to=to, from_=belvedere, body=body)
        print(message.sid)
    except Exception as e:
        print(e)

    msg_cc(to, body)


def msg_alert(who, body):
    incoming = 'msg from ' + who + ': ' + body
    if who not in nassau:
        try:
            message = client.messages.create(to=nassau, from_=belvedere, body=incoming)
            print(message.sid)
        except Exception as e:
            print(e)


def msg_cc(who, body):
    print('cc')
    outgoing = 'msg to ' + who + ': ' + body
    if who not in nassau:
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
    app.run(host='0.0.0.0', port= 5531, debug=True)
