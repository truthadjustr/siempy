import redis
import pysnmp
import time
import json
from libs.sendtrap import *

r = redis.StrictRedis(host = "cache")
pubsub = r.pubsub()
pubsub.subscribe("failedlogon")

print("failedlogon is ready")

while True:
    for eventlog in pubsub.listen():
        if isinstance(eventlog['data'], bytes):
            obj = json.loads(eventlog['data'])
            msg = obj['message']
            s = msg.split(' ')
            ipaddr = s[0]
            r.hincrby('failedlogons_count',ipaddr,1)
            k = 'failedlogon_' + str(ipaddr)
            count = r.incr(k)
            r.expire(k,60)
            if count == 4:
                print("ALERT failed logon!")
                sendtrap_failedlogon()
