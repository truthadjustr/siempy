import redis
import pysnmp
import time
import json
from pysnmp.hlapi import *

def sendtrap():
    errorIndication, errorStatus, errorIndex, varBinds = next(
        sendNotification(
            SnmpEngine(),
            CommunityData('public'),
            UdpTransportTarget(('172.25.0.11',162)),
            ContextData(),
            'trap',
            NotificationType(
                ObjectIdentity('1.3.6.1.6.3.1.1.5.2')
            ).addVarBinds(
                ('1.3.6.1.6.3.1.1.4.3.0','1.3.6.1.4.1.20408.4.1.1.2'),
                ('1.3.6.1.2.1.1.1.0',OctetString('my system'))
            )
        )
    )

    if errorIndication:
        print(errorIndication)

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
                sendtrap()
