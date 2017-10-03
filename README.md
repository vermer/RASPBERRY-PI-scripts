## raspberryPI-scripts

Few simple script to make easier life with Raspberry PI.

### 1.Installation

### 2. checkDelugeAlive.sh

Script to detect if deluge-daemon is up and running and to start it incase of some problems. Script is added to `crontab.bak` file and it is run every 5 minutes according do default configuration. Can be easily change in this file.


`*/5 * * * * /home/pi/RASPBERRY-PI-scripts/checkDelugeAlive.sh`

### 3. crontab.bak

This file is set of jobs to run on your local raspberry pi.
1. `*/2 * * * * /home/pi/RASPBERRY-PI-scripts/Localization.py` every 2 minutes we running script to check our localization via IP address and send us a [Telegram](https://telegram.org/apps) message
2. `*/5 * * * * /home/pi/RASPBERRY-PI-scripts/checkDelugeAlive.sh` every 5 minutes we running script to check if deluge is up and running and if isn't just restart it.
3. `*/5 * * * * /home/pi/RASPBERRY-PI-scripts/napi.py /media/wd/completed/` every 5 minutes we running subtitles downloading  script for specific directory
4. `* 1 * * * /home/pi/RASPBERRY-PI-scripts/update.sh` simple script to update and upgrade raspberry pi system
5. `@daily git pull /home/pi/RASPBERRY-PI-scripts/` update RASPBERRY-PI-scripts from `master`
6. `@daily crontab /home/pi/RASPBERRY-PI-scripts/crontab.bak` restore newest version of crontab
7. `@weekly /sbin/shutdown -r now` reboot system every Sunday 00:00

### 4. instalation.sh
### 5. Localization.py
### 6. napi.py
### 7. sshReverseTunneling.sh
### 8. update.sh
