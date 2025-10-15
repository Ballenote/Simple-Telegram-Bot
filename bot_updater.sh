#!/bin/sh

git pull

if [ "$1" = "1" ]; then 
    #used in crontab after checking for updates and installing them
    sudo reboot
fi

exit 0