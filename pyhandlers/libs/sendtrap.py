import pysnmp
import json
from pysnmp.hlapi import *

def sendtrap_failedlogon():
    errorIndication, errorStatus, errorIndex, varBinds = next(
        sendNotification(
            SnmpEngine(),
            CommunityData('public'),
            UdpTransportTarget(('172.25.0.3',162)),
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
