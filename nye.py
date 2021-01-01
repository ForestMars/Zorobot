#!/usr/bin/env python
# -*- coding: utf-8 -*-
# nye.py (smsbot) - New Year's messenger.
__version__ = '0.1'

import os
import csv
import json
import logging
import shlex
import subprocess
import sys
from random import choice
import time

#import redis
import requests
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client

#import contacts
from common.lumberjack import Log as log
from common.utils import ddict, HaltException as HX
from common import utils


#command = shlex.split("env -i bash -c 'source env/env.sh && env'")
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

HOST = '3.137.143.152'
DOMAIN = 'scheduler'
nassau='+15166982705'
upstate="+18458680258"
belvedere="+14157122019"

#r = redis.StrictRedis(host=redis_host, port=redis_port, password=redis_password, decode_responses=True)
#r.set('counter', 1)

def csv_to_dict(file):
    """ write key val csv to dict. """
    #mydict = {y[0]: y[1] for y in [x.split(",") for x in open(file).read().split('\n') if x]}
    with open(file) as f:
        d = dict(filter(None, csv.reader(f)))

    return d


def csv_to_dict_(file):
    """ write multi-valued csv to dict. """
    with open(file, mode='r') as infile:
        reader = csv.reader(infile)
        with open(file, mode='w') as outfile:
            writer = csv.writer(outfile)
            newdict = {rows[0]:rows[1] for rows in reader}
            return newdict

def rev_dict(dict):
    inv_dict = {v: k for k, v in dict.items()}

    return inv_dict


def prexix_number(number):
    number = str(number.strip(' ').strip('+'))
    """
    if len(number) == 11 and number.startswith('1'):
        return number.strip('1', 1)
    elif len(number) == 10 and not number.startswith('1'):
        return number
    """
    if len(number) == 11 and number.startswith('1'):
        return number
    elif len(number) == 10 and not number.startswith('1'):
        return '1' + number

def validate_number(number):
    number = str(number.strip(' ').strip('+'))

    if len(number) == 11 and number.startswith('1'):
        return number.strip('1', 1)
    elif len(number) == 10 and not number.startswith('1'):
        return number

def send_msg(to, body):
    sys.exit()
    """ Send SMS reply via API """
    try:
        message = client.messages.create(to=to, from_=belvedere, body=body)
        print(message.sid)
    except Exception as e:
        print(e)


def ny_greet(peops, msg):
    sys.exit()
    for who, to in peops.items(): # grrr
        message = ''
        to = validate_number(to)
        messsage = 'HAPPY NEW YEAR ' + who + '! 🎉' + msg
        try:
            send_msg(to, msg)
        except Exception as e:
            log(e)

    print("messages sent.")


if __name__ == "__main__":
    #mydict = csv_to_dict('contacts.csv')
    peops = csv_to_dict('contacts2.csv')
    rev_p = rev_dict(peops)
    print(rev_p)
    #msg = "Wishing you the very VERY best in 2021!! "
    #ny_greet(peops, msg)
