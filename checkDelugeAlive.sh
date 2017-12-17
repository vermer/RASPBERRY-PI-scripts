#!/bin/bash

# Script to detect if deluge-daemon is up and running and to start it incase of
# some problems. Script is added to crontab.bak file and it is runned evry 5 minuts
# according do default configuration. Can be easly change in this file.

#!/bin/bash
ps cax | grep deluged
if [ $? -eq 0 ]; then
  echo "Process is running."
else
  echo "Process is not running."
fi
