#!/bin/sh
# 

export LD_LIBRARY_PATH=/usr/local/lib
snmpd -Lsd -C -c /root/snmpd.conf &
python /root/siemevent.py &
sleep infinity
echo "---oOo--snmpagent--oOo---"

