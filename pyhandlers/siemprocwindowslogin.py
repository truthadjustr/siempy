import redis
import pysnmp
import time
import json
import socket
from libs.sendtrap import *

'''
{
             "message" => "<11>Dec 27 12:44:34 Siem_Server MSWinEventLog   3       Security        1933    Wed Dec 27 12:44:34 2017        4625    Microsoft-Windows-Security-Auditing     N/A     N/A     Failure Audit   Siem_Server     N/A             An account failed to log on.    Subject:   Security ID:  S-1-0-0   Account Name:  -   Account Domain:  -   Logon ID:  0x0    Logon Type:   3    Account For Which Logon Failed:   Security ID:  S-1-0-0   Account Name:  guest   Account Domain:      Failure Information:   Failure Reason:  %%2313   Status:   0xc000006d   Sub Status:  0xc000006a    Process Information:   Caller Process ID: 0x0   Caller Process Name: -    Network Information:   Workstation Name: \\164.52.24.142   Source Network Address: 164.52.24.142   Source Port:  60085    Detailed Authentication Information:   Logon Process:  NtLmSsp    Authentication Package: NTLM   Transited Services: -   Package Name (NTLM only): -   Key Length:  0    This event is generated when a logon request fails. It is generated on the computer where access was attempted.    The Subject fields indicate the account on the local system which requested the logon. This is most commonly a service such as the Server service, or a local process such as Winlogon.exe or Services.exe.    The Logon Type field indicates the kind of logon that was requested. The most common types are 2 (interactive) and 3 (network).    The Process Information fields indicate which account and process on the system requested the logon.    The Network Information fields indicate where a remote logon request originated. Workstation name is not always available and may be left blank in some cases.    The authentication information fields provide detailed information about this specific logon request.   - Transited services indicate which intermediate services have participated in this logon request.   - Package name indicates which sub-protocol was used among the NTLM protocols.   - Key length indicates the length of the generated session key. This will be 0 if no session key was requested.      5925",
                "host" => "172.25.0.1",
        "redischannel" => "siemprocwindowslogin",
            "@version" => "1",
    "syslog_timestamp" => "Dec 27 12:44:34",
              "ipaddr" => "164.52.24.142",
                "prio" => "11",
         "workstation" => "164.52.24.142",
          "@timestamp" => 2017-12-27T05:52:23.726Z,
             "srcport" => "60085"
}

'''

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
        if eventlog['type'] != 'message': continue

        obj = json.loads(eventlog['data'])

        try:
            workstation = obj['workstation']
            remoteIp = obj['ipaddr']
            host = obj['workstation'] # ?
            #print(workstation)

            r.sadd('rfnSiemWindowsLoginIntruder',remoteIp) 

            k = 'siemprocwindowslogin_' + str(remoteIp)
            count = r.incr(k)
            r.expire(k,60)

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
