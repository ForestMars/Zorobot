#!/usr/bin/env python
# config/redis - Configruation for any modeules loading redis.
__version__ = '0.1'

import os

import redis

os.environ['REDIS_HOST'] = "localhost"
os.environ['REDIS_PORT'] = '6379'

redis_host = os.environ['REDIS_HOST']
redis_port = os.environ['REDIS_PORT']
redis_password = os.environ['REDIS_SECRET'] = ''
r = redis.StrictRedis(host=redis_host, port=redis_port, password=redis_password, decode_responses=True)
