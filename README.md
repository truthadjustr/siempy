SIEM in Python
==============

*"To protect that which matters most"*

This is a containerized solution of the log correlator software. It uses the input/output 
and **GROK** filtering of **Logstash**. The configured input is in syslog and the configured
output is also in syslog. In the current design, configured output destination is the **Graylog** server. The
Logstash receiving input is the best place in order to have full control. The default control
provided by Graylog in its web interface is too limiting. 

An **SNMP** service is also provided. The **Redis** cache serves a the in-memory hash map key value 
store that works in tandem with the python programming logic.
