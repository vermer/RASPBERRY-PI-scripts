#!/bin/bash

# Script to detect if deluge-daemon is up and running and to start it incase of
# some problems. Script is added to crontab.bak file and it is runned evry 5 minuts
# according do default configuration. Can be easly change in this file.

readonly SCRIPT_NAME=$(basename $0)

now = "$(date)"

err() {
  logger -p user.error -t $SCRIPT_NAME "$@"
}
if $(ps -A | grep -o  "deluged"); then
	sleep 1
else
	err "$now" ": Deluge crashed"
	sudo service deluge-daemon restart
fi
