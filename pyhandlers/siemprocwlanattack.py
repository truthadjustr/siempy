import redis
import pysnmp
import time
import json
import socket
from libs.sendtrap import *

'''

'''

r = redis.StrictRedis(host = "cache")
pubsub = r.pubsub()
pubsub.subscribe("siemprocwlanattack")

print("siemprocwlanattack is ready")

def update_snmpagent():
    snmpmsg = {
        "oident":"rfnSiemJammingSignal",
        "param":""
    }
    r.publish("siemevent",json.dumps(snmpmsg))

while True:
    for eventlog in pubsub.listen():
        if isinstance(eventlog['data'], int): continue

        obj = json.loads(eventlog['data'])
        msg = obj['message']

        try:
            r.incr('siemprocethspoof_count')

            attackermac = obj['attackermac']

            print("VALUES: {0}".format(attackermac)) 

            update_snmpagent()

            trapid = 1
            
            '''
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
            '''
        except:
            print("EXCEPTION: " + str(msg))
