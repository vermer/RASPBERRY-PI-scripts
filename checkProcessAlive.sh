#!/bin/bash

# Script to detect if deluge-daemon is up and running and to start it incase of
# some problems. Script is added to crontab.bak file and it is runned evry 5 minuts
# according do default configuration. Can be easly change in this file.

#!/bin/bash
PROCESS=$1
PIDS=`ps cax | grep $PROCESS | grep -o '^[ ]*[0-9]*'`
if [ -z "$PIDS" ]; then
  echo "Process not running." 1>&2
  exit 1
else
  echo "Process running." 1>&2
  sudo service deluge-daemon restart
  exit 1
fi
