"""
SNMPv1 TRAP with defaults
+++++++++++++++++++++++++

Send SNMPv1 TRAP through unified SNMPv3 message processing framework
using the following options:

* SNMPv1
* with community name 'public'
* over IPv4/UDP
* send TRAP notification
* with Generic Trap #1 (warmStart) and Specific Trap 0
* with default Uptime
* with default Agent Address
* with Enterprise OID 1.3.6.1.4.1.20408.4.1.1.2
* include managed object information '1.3.6.1.2.1.1.1.0' = 'my system'

Functionally similar to:

| $ snmptrap -v1 -c public demo.snmplabs.com 1.3.6.1.4.1.20408.4.1.1.2 0.0.0.0 1 0 0 1.3.6.1.2.1.1.1.0 s "my system"

"""#
from pysnmp.hlapi import *

errorIndication, errorStatus, errorIndex, varBinds = next(
    sendNotification(
        SnmpEngine(),
        #CommunityData('public', mpModel=0), # orig line
        CommunityData('public'), # to make it v2c?
        UdpTransportTarget(('172.17.0.2', 162)),
        ContextData(),
        'trap',
        NotificationType(
            ObjectIdentity('1.3.6.1.4.1.9746.1052.900.0.6')
        ).addVarBinds(
            ('1.3.6.1.4.1.9746.10252.900.1.5.0', Integer(69)),
            ('1.3.6.1.2.1.1.1.0', OctetString('my system')),
            ("1.3.6.1.4.1.9746.10252.900.1.19.0", OctetString("hostname_here")),
            ("1.3.6.1.4.1.9746.10252.900.1.20.0", OctetString("ipaddr_here")),
            ("1.3.6.1.4.1.9746.10252.900.1.21.0", Integer(13))
        )
    )
)

if errorIndication:
    print(errorIndication)
