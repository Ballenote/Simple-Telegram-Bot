import os
import subprocess
import telebot
import requests
from dotenv import load_dotenv

# loading secrets
load_dotenv("secrets.env")
BOT_TOKEN = os.getenv("BOT_TOKEN")
USER_ID = os.getenv("USER_ID")



def user_verification(uuid):
    #only my user ID can use the bot 
    if (uuid == (int(USER_ID))):
        return True


if __name__=="__main__":

    bot = telebot.TeleBot(BOT_TOKEN)

    bot.send_message(USER_ID, "The bot is back online.")

    @bot.message_handler(commands=['start'])
    def send_welcome(message):
        if (user_verification(message.from_user.id) == True):
            bot.reply_to(message, "Welcome")

##############################################
##              VPN ACTIONS                 ##
##############################################

    @bot.message_handler(commands=['vpn_up'])
    def handle(message):
        if (user_verification(message.from_user.id) == True):
            result = subprocess.run(["python", "vpn.py", "up"],capture_output=True, text=True)
            bot.reply_to(message,result.stdout)


    @bot.message_handler(commands=['vpn_down'])
    def handle(message):
        if (user_verification(message.from_user.id) == True):
            result = subprocess.run(["python", "vpn.py", "down"],capture_output=True, text=True)
            bot.reply_to(message,result.stdout)
            
    @bot.message_handler(commands=['vpn_info'])
    def handle(message):
        if (user_verification(message.from_user.id) == True):
            result = subprocess.run(["python", "vpn.py", "info"],capture_output=True, text=True)
            bot.reply_to(message,result.stdout, parse_mode='Markdown')
            
##############################################
##              SSH ACTIONS                 ##
##############################################
    @bot.message_handler(commands=['ssh_up'])
    def handle(message):
        if (user_verification(message.from_user.id) == True):
            result = subprocess.run(["python", "ssh.py", "up"],capture_output=True, text=True)
            bot.reply_to(message,result.stdout)


    @bot.message_handler(commands=['ssh_down'])
    def handle(message):
        if (user_verification(message.from_user.id) == True):
            result = subprocess.run(["python", "ssh.py", "down"],capture_output=True, text=True)
            bot.reply_to(message,result.stdout)
    
    @bot.message_handler(commands=['ssh_status'])
    def handle(message):
        if (user_verification(message.from_user.id) == True):
            result = subprocess.run(["python", "ssh.py", "status"],capture_output=True, text=True)
            bot.reply_to(message,result.stdout)

    @bot.message_handler(commands=['ssh_info'])
    def handle(message):
        if (user_verification(message.from_user.id) == True):
            result = subprocess.run(["python", "ssh.py", "info"],capture_output=True, text=True)
            bot.reply_to(message,result.stdout, parse_mode='Markdown')
            
    @bot.message_handler(commands=['ssh_add'])
    def handle(message):
        if (user_verification(message.from_user.id) == True):
            bot.reply_to(message,"Paste the public key found by doing \n`cat ~/.ssh/raspberry.pub`\n or write <No> to abort",parse_mode='Markdown')
            bot.register_next_step_handler(message,step2)
    def step2(message):
        if (user_verification(message.from_user.id) == True):
            nos=["no","nO","No","NO"]
            if message.text in nos:
                bot.reply_to(message,"Operation aborted")
            else:
                result = subprocess.run(["python", "ssh.py", "add",message.text],capture_output=True, text=True)
                bot.reply_to(message,result.stdout)

##############################################
##              MISC ACTIONS                ##
##############################################
    @bot.message_handler(commands=['update'])
    def handle(message):
        if (user_verification(message.from_user.id) == True):
            result = subprocess.run(
            ["python","misc.py", "update"],
            capture_output=True,
            text=True
            )
            bot.reply_to(message,  result.stdout)

    @bot.message_handler(commands=['reboot'])
    def handle(message):
        if (user_verification(message.from_user.id) == True): 
            subprocess.run(["python","misc.py","reboot"])
            
    bot.infinity_polling()
