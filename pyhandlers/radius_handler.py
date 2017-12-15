import redis
import pysnmp
import time

r = redis.StrictRedis(host = "cache")
pubsub = r.pubsub()
pubsub.subscribe("radius")

print("radius is ready")

while True:
    for eventlog in pubsub.listen():
        print(eventlog['data'])

