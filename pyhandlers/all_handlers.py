import redis
import pysnmp
import time
import json

#r = redis.StrictRedis(host = "cache")
r = redis.StrictRedis(host = "172.17.0.3")
pubsub = r.pubsub()
pubsub.subscribe([
    "webconfig",
    "failedlogon",
    "foundrogueap",
    "lostrogueap",
    "interference",
    "radius"
])

def do_webconfig(data):
    print('webconfig: ' + str(data))

def do_failedlogon(data):
    print('failedlogon: ' + str(data))

def do_foundrogueap(data):
    print('foundrogueap: ' + str(data))

def do_lostrogueap(data):
    print('flostrogueap: ' + str(data))

def do_interference(data):
    print('interference: ' + str(data))

def do_radius(data):
    print('radius: ' + str(data))

print("all is ready")

while True:
    for eventlog in pubsub.listen():
        if isinstance(eventlog['data'], bytes):
            msg = eventlog['data']
            if eventlog['channel'] == 'webconfig':
                do_webconfig(msg)
            elif eventlog['channel'] == 'failedlogon':
                do_failedlogon(msg)
            elif eventlog['channel'] == 'foundrogueap':
                do_foundrogueap(msg)
            elif eventlog['channel'] == 'lostrogueap':
                do_lostrogueap(msg)
            elif eventlog['channel'] == 'interference':
                do_interference(msg)
            elif eventlog['channel'] == 'radius':
                do_radius(msg)
