import redis
import pysnmp
import time
import json
import socket
from libs.sendtrap import *

r = redis.StrictRedis(host = "cache")
pubsub = r.pubsub()
pubsub.subscribe("siemprocwindowslogin")

def update_snmpagent(count,remoteIp):
    snmpmsg = {
        "oident":"rfnSiemWindowsLoginIntruder", 
        "param":[remoteIp]
    }
    r.publish("siemevent",json.dumps(snmpmsg))

print("siemprocwindowslogin is ready")

while True:
    for eventlog in pubsub.listen():
        if isinstance(eventlog['data'], int): continue

        obj = json.loads(eventlog['data'])
        msg = obj['message']

        try:
            splits = msg.split(' ')
            remoteIp = splits[0]

            r.sadd('rfnSiemWindowsLoginIntruder',remoteIp) 
            r.hincrby('siemprocwindowslogin_hitcount',remoteIp,1)

            k = 'failedlogon_' + str(remoteIp)
            count = r.incr(k)
            r.expire(k,60)
            
            host = socket.gethostname()

            update_snmpagent(count,remoteIp)

            if count == 4:
                print("ALERT failed logon!")

                trapid = 6
                varbinds = (
                    ('1.3.6.1.4.1.9746.10252.900.1.5.0',Integer(0)),    
                    ('1.3.6.1.4.1.9746.10252.900.1.19.0',OctetString(host)),    
                    ('1.3.6.1.4.1.9746.10252.900.1.20.0',OctetString(remoteIp)),    
                    ('1.3.6.1.4.1.9746.10252.900.1.21.0',Integer(count))    
                )
                sendtrap(trapid,varbinds)
        except:
            print("EXCEPTION: " + str(msg))
