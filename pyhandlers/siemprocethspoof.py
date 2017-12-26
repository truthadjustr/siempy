import redis
import pysnmp
import time
import json
import socket
from libs.sendtrap import *

'''
{
      "@timestamp" => 2017-12-26T09:41:54.110Z,
         "message" => "<105>  id=firewall sn=C0EAE4F5F08E time=\"2017-12-26 17:41:16\" fw=0.0.0.0 pri=1 c=32 gcat=6 m=1209 srcMac=08:00:27:43:1f:10 src=10.7.1.19:46897:X0 srcZone=LAN dstMac=c0:ea:e4:f5:f0:8e dst=165.21.83.88:53 proto=udp/dns rcvd=72 n=81708 fw_action=\"NA\"",
              "x0" => "X0",
            "time" => "2017-12-26 17:41:16",
        "@version" => "1",
              "id" => "firewall",
              "fw" => "0.0.0.0",
               "c" => "32",
            "host" => "10.7.1.150",
             "dst" => "165.21.83.88:53",
           "proto" => "udp/dns",
            "gcat" => "6",
       "fw_action" => "NA",
    "redischannel" => "siemprocethspoof",
          "srcMac" => "08:00:27:43:1f:10",
             "pri" => [
        [0] "105",
        [1] "1"
    ],
            "rcvd" => "72",
             "src" => "10.7.1.19:46897",
         "srcZone" => "LAN",
               "n" => "81708",
          "dstMac" => "c0:ea:e4:f5:f0:8e"
}
'''

r = redis.StrictRedis(host = "cache")
pubsub = r.pubsub()
pubsub.subscribe("siemprocethspoof")

print("siemprocethspoof is ready")

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
            id = obj['id']
            srcMac = obj['srcMac']
            srcZone = obj['srcZone']
            n = obj['n']
            dstMac = obj['dstMac']

            print("VALUES: {0} {1} {2} {3} {4}".format(id,srcMac,srcZone,n,dstMac)) 

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
