import redis
import pysnmp
import time

r = redis.StrictRedis(host = "cache")
pubsub = r.pubsub()
pubsub.subscribe("interference")

print("interference is ready")

while True:
    for eventlog in pubsub.listen():
        print(eventlog['data'])
        r.incr('interference_count')
