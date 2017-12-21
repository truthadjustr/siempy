import redis
import time
import json

##########################################################
# this python listener must be running beside snmpd daemon
# inside the snmpagent container. It writes to /var/siem/*
# to feed snmp data to our customized snmpd daemon

BASEDIR = "/var/siem/"

while True:
    try:
        r = redis.StrictRedis(host = 'cache')
        pubsub = r.pubsub()
        pubsub.subscribe('siemevent')
        break
    except:
        print("reconnecting in 5s ...")
        time.sleep(5)
        continue

def rfnSiemJammingSignal(p):
    target = BASEDIR + "rfnSiemJammingSignalList"
    items = r.smembers('rfnSiemJammingSignal')
    count = r.scard('rfnSiemJammingSignal')

    with open(target, "w") as t:
    	for item in items:
       	    t.write(item + "\n")

    target = BASEDIR + "rfnSiemJammingSignalListCount"
    with open(target, "w") as t:
        t.write(str(count))

def rfnSiemRogueAp(p):
    target = BASEDIR + "rfnSiemRogueApList"
    items = r.smembers('rfnSiemRogueAp')
    count = r.scard('rfnSiemRogueAp')

    with open(target, "w") as t:
    	for item in items:
       	    t.write(item + "\n")

    target = BASEDIR + "rfnSiemRogueApListCount"
    with open(target, "w") as t:
        t.write(str(count))

def rfnSiemWindowsLoginIntruder(p):
    target = BASEDIR + "rfnSiemWindowsLoginIntruderList"
    items = r.smembers('rfnSiemWindowsLoginIntruder')
    count = r.scard('rfnSiemWindowsLoginIntruder')

    with open(target, "w") as t:
    	for item in items:
       	    t.write(item + "\n")

    target = BASEDIR + "rfnSiemWindowsLoginIntruderListCount"
    with open(target, "w") as t:
        t.write(str(count))


def rfnSiemWlcLoginIntruder(p):
    target = BASEDIR + "rfnSiemWlcLoginIntruderList"
    items = r.smembers('rfnSiemWlcLoginIntruder')
    count = r.scard('rfnSiemWlcLoginIntruder')

    with open(target, "w") as t:
    	for item in items:
       	    t.write(item + "\n")

    target = BASEDIR + "rfnSiemWlcLoginIntruderListCount"
    with open(target, "w") as t:
        t.write(str(count))

def rfnSiemWlcRadiusLoginIntruder(p):
    target = BASEDIR + "rfnSiemWlcRadiusLoginIntruderList"
    items = r.smembers('rfnSiemWlcRadiusLoginIntruder')
    count = r.scard('rfnSiemWlcRadiusLoginIntruder')

    with open(target, "w") as t:
    	for item in items:
       	    t.write(item + "\n")

    target = BASEDIR + "rfnSiemWlcRadiusLoginIntruderListCount"
    with open(target, "w") as t:
        t.write(str(count))

def rfnSiemWlcWiredAttack(p):
    target = BASEDIR + "rfnSiemWlcWiredAttackList"
    items = r.smembers('rfnSiemWlcWiredAttack')
    count = r.scard('rfnSiemWlcWiredAttack')

    with open(target, "w") as t:
    	for item in items:
       	    t.write(item + "\n")

    target = BASEDIR + "rfnSiemWlcWiredAttackListCount"
    with open(target, "w") as t:
        t.write(str(count))

def rfnSiemWlcWlanAttack(p):
    target = BASEDIR + "rfnSiemWlcWlanAttackList"
    items = r.smembers('rfnSiemWlcWlanAttack')
    count = r.scard('rfnSiemWlcWlanAttack')

    with open(target, "w") as t:
    	for item in items:
       	    t.write(item + "\n")

    target = BASEDIR + "rfnSiemWlcWlanAttackListCount"
    with open(target, "w") as t:
        t.write(str(count))

dispatchTable = {
    'rfnSiemJammingSignal':rfnSiemJammingSignal,
    'rfnSiemRogueAp':rfnSiemRogueAp,
    'rfnSiemWindowsLoginIntruder':rfnSiemWindowsLoginIntruder,
    'rfnSiemWlcLoginIntruder':rfnSiemWlcLoginIntruder,
    'rfnSiemWlcRadiusLoginIntruder':rfnSiemWlcRadiusLoginIntruder,
    'rfnSiemWlcWiredAttack':rfnSiemWlcWiredAttack,
    'rfnSiemWlcWlanAttack':rfnSiemWlcWlanAttack,
}

print('siemevent is now listening ...')

while True:
    for event in pubsub.listen():
        if not isinstance(event['data'],bytes): continue
        try:
            e = json.loads(str(event['data'])) 

            F = open("/tmp/event.log","a")
            F.write(str(e) + "\n")
            F.close()

            fn = e['oident']
            param = e['param'] # TODO must pass all json
            if fn in dispatchTable:
                print("=> " + fn)
                dispatchTable[fn](param)
            else:
                print("noimpl")
        except Exception, e:
            print("EXCEPTION: " + str(e))
            F = open("/tmp/event.log","a")
            F.write("EXCEPTION: " + str(e) + "\n")
            F.close()
