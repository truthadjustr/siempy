SIEM in Python
==============

This is a containerized solution of the log correlator software. It uses the input/output 
and **GROK** filtering of **Logstash**. The configured input is in syslog and the configured
output is also in syslog. In the current design, configured output destination is the **Graylog** server. The
Logstash receiving input is the best place in order to have full control. The default control
provided by Graylog in its web interface is too limiting. 

An **SNMP** service is also provided. The **Redis** cache serves a the in-memory hash map key value 
store that works in tandem with the python programming logic.

**The Main Orchestrator File**
./docker-compose.yml

**Shared folder for Logstash:**
./log
./log/udp_5140.log

**Handlers for each string pattern found by grok:**

./pyhandlers
./pyhandlers/siemprocrogueap.py
./pyhandlers/siemprocwlcradiuslogin.py
./pyhandlers/siemprocwindowslogin.py
./pyhandlers/siemprocwlclogin.py
./pyhandlers/siemprocjamming.py

**Common function library:**
./pyhandlers/libs
./pyhandlers/libs/sendtrap.py
./pyhandlers/libs/__init__.py

**Container Prep:**
./containers/siempy/Dockerfile
./containers/siemcorr/Dockerfile

**Shared Folder for t252snmpagent:**
./var.siem

**Logstash Configuration:**
./correlator
./correlator/recognizer.conf

**Code Snippet References:**
./reference
./reference/default-v1-trap2.py
./reference/v2c-trap-with-notification-objects.py
./reference/test.py
./reference/pass_persist.py
./reference/container-test.c

**SNMP Agent Config:**
./t252snmpagent
./t252snmpagent/entrypoint.sh
./t252snmpagent/siemevent.py
./t252snmpagent/snmpd.conf
