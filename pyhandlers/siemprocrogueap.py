import redis
import pysnmp
import time
import json
import socket
from libs.sendtrap import *

r = redis.StrictRedis(host = "cache")
pubsub = r.pubsub()
pubsub.subscribe(["siemprocrogueap_found","siemprocrogueap_lost"])

print("siemprocrogueap is ready")

while True:
    for eventlog in pubsub.listen():
        if isinstance(eventlog['data'], int): continue

        obj = json.loads(eventlog['data'])
        msg = obj['message']

        try:
            print(eventlog['data'])
            r.incr('siemprocrogueap_count')
            splits = msg.split(' ')
            host = socket.gethostname()

            if "Found Rogue AP!" in msg:
                rogueMac  = splits[6]
                frequency = int(splits[9])
                ssid      = splits[15].replace("\n","")

                trapid = 2
                varbinds = (
                    ('1.3.6.1.4.1.9746.10252.900.1.5.0',Integer(0)),
                    ('1.3.6.1.4.1.9746.10252.900.1.1.0',OctetString(host)),
                    ('1.3.6.1.4.1.9746.10252.900.1.2.0',OctetString(rogueMac)),
                    ('1.3.6.1.4.1.9746.10252.900.1.4.0',Integer(frequency)),
                    ('1.3.6.1.4.1.9746.10252.900.1.3.0',OctetString(ssid))
                    
                )
                sendtrap(trapid,varbinds)


            elif "Lost Rogue AP" in msg:
                rogueMac = splits[6]
                ssid     = splits[9].replace("\n","")
                isFound  = False

                trapid = 3
                varbinds = (
                    ('1.3.6.1.4.1.9746.10252.900.1.5.0',Integer(0)),
                    ('1.3.6.1.4.1.9746.10252.900.1.1.0',OctetString(host)),
                    ('1.3.6.1.4.1.9746.10252.900.1.2.0',OctetString(rogueMac)),
                    ('1.3.6.1.4.1.9746.10252.900.1.3.0',OctetString(ssid))
                )
                sendtrap(trapid,varbinds)
        except:
            print("EXCEPTION: " + str(msg))
