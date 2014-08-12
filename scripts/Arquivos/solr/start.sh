#!/bin/bash

# Directory where solr is installed
SOLR_HOME=/usr/share/solr/example

# Java options for Solr
OPTIONS="-Xmx1024m"

# Path to pid file
PIDFILE=/var/run/solr.pid

# Path to log file
LOG_FILE=/var/log/solr.log

COMMAND="java $OPTIONS -jar start.jar"

cd $SOLR_HOME
nohup $COMMAND > $LOG_FILE 2>&1 &
echo $! > $PIDFILE
exit $?
