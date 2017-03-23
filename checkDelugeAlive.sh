#!/bin/bash

readonly SCRIPT_NAME=$(basename $0)
now="$(date)"

err() {
  logger -p user.error -t $SCRIPT_NAME "$@"
}

if $(ps -A | grep -o  "deluged"); then
	sleep 1
else
	err "$now" ": Deluge crashed"
	sudo service deluge-daemon restart
fi
