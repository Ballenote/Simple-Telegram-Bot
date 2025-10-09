#/bin/sh
#to be placed in /Documents
cd ~/Documents/Simple-Telegram-Bot
git pull

if [ "$1" = "1" ]; then 
    sudo reboot
fi
exit 0