import telebot
import requests 
import os
import subprocess
from dotenv import load_dotenv

#loading secrets
load_dotenv("secrets.env") 
BOT_TOKEN=os.getenv("BOT_TOKEN")
USER_ID=os.getenv("USER_ID")
PUB_KEY=os.getenv("PUB_KEY")

def user_verification(uuid):
    if(uuid==(int(USER_ID))):
        return True
    else:
        print(2)
        return False

bot=telebot.TeleBot(BOT_TOKEN)
@bot.message_handler(commands=['start'])
def send_welcome(message):
    if(user_verification(message.from_user.id)==True):
        bot.reply_to(message, "Welcome")

@bot.message_handler(commands=['info'])
def handle(message):
    if(user_verification(message.from_user.id)==True):
        pubip=requests.get("https://ifconfig.me/").text
        bot.reply_to(message, f"The public IP is: {pubip}\nThe WireGuard port is 40959\nThe public key is {PUB_KEY}")

@bot.message_handler(commands=['vpn_up'])
def handle(message):
    if(user_verification(message.from_user.id)==True):
        try:
            result = subprocess.run(
            ["sudo",'wg-quick', 'up', 'wg0'],  
            check=True,                    
            stdout=subprocess.PIPE,        
            stderr=subprocess.PIPE,        
            text=True                      
            )
            bot.reply_to(message, "the VPN is now active")

        except subprocess.CalledProcessError as e:
            bot.reply_to(message,  e.stderr)
    
@bot.message_handler(commands=['vpn_down'])
def handle(message):
    if(user_verification(message.from_user.id)==True):
        try:
            result = subprocess.run(
            ["sudo",'wg-quick', 'down', 'wg0'],  
            check=True,                    
            stdout=subprocess.PIPE,        
            stderr=subprocess.PIPE,        
            text=True                      
            )
            bot.reply_to(message, "the VPN is now deactivated")

        except subprocess.CalledProcessError as e:
            bot.reply_to(message,  e.stderr)
    
    

bot.infinity_polling()