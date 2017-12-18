import redis
import pysnmp
import time
from libs.sendtrap import *

r = redis.StrictRedis(host = "cache")
pubsub = r.pubsub()
pubsub.subscribe("siemprocjamming")

print("siemprocjamming is ready")

while True:
    for eventlog in pubsub.listen():
        if isinstance(eventlog['data'], bytes):
            print(eventlog['data'])
            r.incr('siemprocjamming_count')
