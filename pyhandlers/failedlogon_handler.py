import redis
import pysnmp
import time

r = redis.StrictRedis(host = "cache")
#r = redis.StrictRedis(host = "172.17.0.2")
pubsub = r.pubsub()
pubsub.subscribe("failedlogon")

print("failedlogon is ready")

while True:
    for eventlog in pubsub.listen():
        # if eventlog['data'] != 1:
            print(eventlog['data'])
            msg = str(eventlog['data'])
            s = msg.split(' ')
            ipaddr = s[0]
            r.hincrby('failedlogons_count',ipaddr,1)
            k = 'failedlogon_' + str(ipaddr)
            #r.setex(k,60,msg)
            count = r.incr(k)
            r.expire(k,10)
            #print("count = %d" % count) 
            if count > 3:
                #r.setex(k,60,msg) 
                print("ALERT failed logon!")
