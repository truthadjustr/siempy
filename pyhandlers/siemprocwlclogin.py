import redis
import pysnmp
import time
import json
import socket
from libs.sendtrap import *

r = redis.StrictRedis(host = "cache")
pubsub = r.pubsub()
pubsub.subscribe("siemprocwlclogin")

print("siemprocwlclogin is ready")

while True:
    for eventlog in pubsub.listen():
        if isinstance(eventlog['data'], int): continue

        obj = json.loads(eventlog['data'])
        msg = obj['message']

        try:
            print(eventlog['data'])
            r.incr('siemprocwlclogin_count')
            splits = msg.split(' ')
            remoteIp = splits[7]
            key = 'siemprocwlclogin_' + str(remoteIp)
            count = r.incr(key)
            r.expire(key,60)

            host = socket.gethostname()

            if count == 4:
                print("ALERT siemprocwlcloglin by " + str(remoteIp))
                trapid = 7
                varbinds = (
                    ('1.3.6.1.4.1.9746.10252.900.1.5.0',Integer(0)),
                    ('1.3.6.1.4.1.9746.10252.900.1.19.0',OctetString(host)),   
                    ('1.3.6.1.4.1.9746.10252.900.1.22.0',OctetString(remoteIp)),   
                    ('1.3.6.1.4.1.9746.10252.900.1.21.0',Integer(count))
                )
                sendtrap(trapid,varbinds)
        except:
            print("EXCEPTION: " + str(msg))
