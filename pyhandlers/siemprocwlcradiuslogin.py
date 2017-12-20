import redis
import pysnmp
import time
import json
import socket
from libs.sendtrap import *

r = redis.StrictRedis(host = "cache")
pubsub = r.pubsub()
pubsub.subscribe("siemprocwlcradiuslogin")

print("siemprocwlcradiuslogin is ready")

def update_snmpagent():
    snmpmsg = {
        "oident":"rfnSiemWlcRadiusLoginIntruder",
        "param":""
    }
    r.publish("siemevent",json.dumps(snmpmsg))

while True:
    for eventlog in pubsub.listen():
        if isinstance(eventlog['data'], int): continue
    
        obj = json.loads(eventlog['data'])
        log = obj['message']

        try:
            print(eventlog['data'])
            r.incr('siemprocwlcradiuslogin_count')
            splits = log.split(' ')
            remoteIp = splits[9]
            username = splits[7].strip("'")
            key = 'siemprocwlcradiuslogin_' + str(remoteIp)
            count = r.incr(key)
            r.expire(key,60)
            host = socket.gethostname()
            update_snmpagent()

            if count == 4:
                print("ALERT Radius failed logon")
                trapid = 9
                varbinds = (
                    ('1.3.6.1.4.1.9746.10252.900.1.5.0',Integer(0)),
                    ('1.3.6.1.4.1.9746.10252.900.1.22.0',OctetString(host)),
                    ('1.3.6.1.4.1.9746.10252.900.1.23.0',OctetString(remoteIp)),
                    ('1.3.6.1.4.1.9746.10252.900.1.24.0',OctetString(username))
                )
                sendtrap(trapid,varbinds)
        except:
            print("EXCEPTION: " + str(log))
