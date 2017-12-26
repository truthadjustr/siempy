import redis
import pysnmp
import time
import json
import socket
from libs.sendtrap import *

'''
{
                 "PRI" => "129",
        "redischannel" => "siemprocjamming",
            "@version" => "1",
                  "nf" => "-89",
               "appid" => "1126",
                 "app" => "APSPECTRAL",
                "rssi" => "37",
                "load" => "16",
    "syslog_timestamp" => "Jan  1 18:37:42",
                "host" => "172.25.0.1",
          "@timestamp" => 2017-12-26T06:45:43.415Z,
             "channel" => "149",
             "message" => "<129>Jan  1 18:37:42 APSPECTRAL[1126]: WARNING! WIFI Interference detected at channel 149 ( 5745MHz ) ( RSSI 37 NF -89 LOAD 16 )\n",
           "megahertz" => "5745"
}
'''

r = redis.StrictRedis(host = "cache")
pubsub = r.pubsub()
pubsub.subscribe("siemprocjamming")

print("siemprocjamming is ready")

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
            pri = obj['PRI']
            nf = obj['nf']
            moduleid = obj['moduleid']
            module = obj['module']
            rssi = obj['rssi']
            load = obj['load']
            channel = obj['channel']
            megahertz = obj['megahertz']

            print("VALUES: {0} {1} {2} {3} {4} {5} {6} {7}".format(pri,nf,moduleid,module,rssi,load,channel,megahertz)) 

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
