import redis
import pysnmp
import time

r = redis.StrictRedis(host = "cache")
pubsub = r.pubsub()
pubsub.subscribe("webconfig")

print("webconfig is ready")

while True:
    for eventlog in pubsub.listen():
        print(eventlog['data'])
