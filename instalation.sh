#!/bin/bash
sudo pip install requests
sudo crontab crontab.bak
sudo cat /var/log/daily-deluge-backup.log
sudo cat /var/log/daily-localization-backup.log
sudo cat /var/log/daily-napi-backup.log
sudo cat /var/log/daily-update-backup.log
