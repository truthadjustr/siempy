import pysnmp
from pysnmp.hlapi import *

def sendtrap(trapid,varbinds):

    SnmpHost = ('172.25.0.2',162)
    objident = '1.3.6.1.4.1.9746.10252.900.0.%d' % trapid

    errorIndication, errorStatus, errorIndex, varBinds = next(
        sendNotification(
            SnmpEngine(),
            CommunityData('public'),
            UdpTransportTarget(SnmpHost),
            ContextData(),
            'trap',
            NotificationType(ObjectIdentity(objident)).addVarBinds(
                *varbinds  
            )
        )
    )

    if errorIndication:
        print(errorIndication)

