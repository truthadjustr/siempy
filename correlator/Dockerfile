FROM docker.elastic.co/logstash/logstash-oss:6.1.0
LABEL ident="truthadjustr/siemcorr"

RUN logstash-plugin install logstash-output-syslog logstash-output-gelf
