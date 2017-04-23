#/bin/sh
while true; do
	sleep $((60*10))
	ssh -f -NT -R 1357:localhost:22 vermer@81.4.120.32
done
