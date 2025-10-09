import os
import subprocess
import telebot
import requests
from dotenv import load_dotenv

# loading secrets
load_dotenv("secrets.env")
BOT_TOKEN = os.getenv("BOT_TOKEN")
USER_ID = os.getenv("USER_ID")
PUB_KEY = os.getenv("PUB_KEY")
PORT = os.getenv("PORT")


def user_verification(uuid):
    #only my user ID can use the bot 
    if (uuid == (int(USER_ID))):
        return True
    else:
        print(2)
        return False


def vpn_action(action):
    #actually turning on or off the Wireguard VPN
    result = subprocess.run(
        ["sudo", 'wg-quick', action, 'wg0'],
        capture_output=True,
        text=True
    )
    return [result.returncode, result.stdout, result.stderr]


bot = telebot.TeleBot(BOT_TOKEN)

bot.send_message(USER_ID, "The bot is back online")

@bot.message_handler(commands=['start'])
def send_welcome(message):
    if (user_verification(message.from_user.id) == True):
        bot.reply_to(message, "Welcome")


@bot.message_handler(commands=['info'])
def handle(message):
    if (user_verification(message.from_user.id) == True):
        pubipv6 = requests.get("https://ifconfig.me/").text
        pubipv4 = subprocess.run(
        ["curl","-4","https://ifconfig.me/"],
        capture_output=True,
        text=True
        ).stdout
        bot.send_message(
            USER_ID, f"The public IPV&/V$ are: \n\n`{pubipv6}`\n\n`{pubipv4}`\n\nThe WireGuard port is \n\n`{PORT}`\n\nThe public key of the server is \n\n`{PUB_KEY}`\n", parse_mode='Markdown')


@bot.message_handler(commands=['vpn_up'])
def handle(message):
    if (user_verification(message.from_user.id) == True):
        result = vpn_action("up")
        if (result[0] == 0):
            bot.reply_to(message, "the VPN is now active")
        elif (result[0] == 1):
            bot.reply_to(message,  result[2])
        else:
            bot.reply_to(message,  result[2])


@bot.message_handler(commands=['vpn_down'])
def handle(message):
    if (user_verification(message.from_user.id) == True):
        result = vpn_action("down")
        if (result[0] == 0):
            bot.reply_to(message, "the VPN is now deactivated")
        elif (result[0] == 1):
            bot.reply_to(message,  result[2])
        else:
            bot.reply_to(message,  result[2])

@bot.message_handler(commands=['update'])
#it could be useful to trigger a remote update on the raspberry
def handle(message):
    if (user_verification(message.from_user.id) == True):
        result = subprocess.run(
        ["sh","/home/casa/Documents/bot_updater.sh", "1"],
        capture_output=True,
        text=True
        )
        if (result.returncode==0):
            bot.reply_to(message,  result.stdout)
            
        else:
            bot.reply_to(message,  result.stderr)

@bot.message_handler(commands=['reboot'])
def handle(message):
    if (user_verification(message.from_user.id) == True): 
        subprocess.run(["sudo","reboot"])
        
bot.infinity_polling()
