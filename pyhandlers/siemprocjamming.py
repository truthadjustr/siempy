import redis
import pysnmp
import time
import json
import socket
from libs.sendtrap import *

r = redis.StrictRedis(host = "cache")
pubsub = r.pubsub()
pubsub.subscribe("siemprocjamming")

print("siemprocjamming is ready")

while True:
    for eventlog in pubsub.listen():
        if isinstance(eventlog['data'], int): continue

        obj = json.loads(eventlog['data'])
        msg = obj['message']

        try:
            print(eventlog['data'])
            r.incr('siemprocjamming_count')
            splits = msg.split(' ')

            host = socket.gethostname()
            jammingType = int(splits[2])
            frequency   = int(splits[7])
            rssi        = int(splits[13])
            noiseFloor  = int(splits[15])
            load        = int(splits[17])

            trapid = 1
            varbinds = (
                ('1.3.6.1.4.1.9746.10252.900.1.5.0',Integer(0)),
                ('1.3.6.1.4.1.9746.10252.900.1.1.0',OctetString(host)),
                ('1.3.6.1.4.1.9746.10252.900.1.6.0',Integer(jammingType)),
                ('1.3.6.1.4.1.9746.10252.900.1.7.0',Integer(frequency)),
                ('1.3.6.1.4.1.9746.10252.900.1.8.0',Integer(rssi)),
                ('1.3.6.1.4.1.9746.10252.900.1.9.0',Integer(noiseFloor)),
                ('1.3.6.1.4.1.9746.10252.900.1.18.0',Integer(load))
            )
            sendtrap(trapid,varbinds) 
        except:
            print("EXCEPTION: " + str(msg))
