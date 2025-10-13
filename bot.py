import os
import subprocess
import telebot
import requests
from dotenv import load_dotenv
import io
import base64

# loading secrets
load_dotenv("secrets.env")
BOT_TOKEN = os.getenv("BOT_TOKEN")
USER_ID = os.getenv("USER_ID")

nos = ["no", "nO", "No", "NO"]


def user_verification(uuid):
    # only my user ID can use the bot
    if (uuid == (int(USER_ID))):
        return True


if __name__ == "__main__":

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
            result = subprocess.run(
                ["python3", "vpn.py", "up"], capture_output=True, text=True)
            bot.reply_to(message, result.stdout)

    @bot.message_handler(commands=['vpn_down'])
    def handle(message):
        if (user_verification(message.from_user.id) == True):
            result = subprocess.run(
                ["python3", "vpn.py", "down"], capture_output=True, text=True)
            bot.reply_to(message, result.stdout)

    @bot.message_handler(commands=['vpn_info'])
    def handle(message):
        if (user_verification(message.from_user.id) == True):
            result = subprocess.run(
                ["python3", "vpn.py", "info"], capture_output=True, text=True)
            bot.reply_to(message, result.stdout, parse_mode='Markdown')

    @bot.message_handler(commands=['vpn_status'])
    def handle(message):
        if (user_verification(message.from_user.id) == True):
            result = subprocess.run(
                ["python3", "vpn.py", "status"], capture_output=True, text=True)
            bot.reply_to(message, result.stdout, parse_mode='Markdown')

    @bot.message_handler(commands=['vpn_list'])
    def handle(message):
        if (user_verification(message.from_user.id) == True):
            result = subprocess.run(
                ["python3", "vpn.py", "list"], capture_output=True, text=True)
            bot.reply_to(message, result.stdout, parse_mode='Markdown')

    @bot.message_handler(commands=['vpn_create'])
    def handle(message):
        if (user_verification(message.from_user.id) == True):
            bot.reply_to(
                message, "Enter the name of the peer you want to create (type No to abort)")
            bot.register_next_step_handler(message, step2_vpn_create)

    def step2_vpn_create(message):
        if (user_verification(message.from_user.id) == True):
            if message.text in nos:
                bot.reply_to(message, "Operation aborted")
            else:
                result = subprocess.run(
                    ["python3", "vpn.py", "create", message.text], capture_output=True, text=True)
                bot.reply_to(message, result.stdout, parse_mode='Markdown')
                step2_vpn_get(message)

    @bot.message_handler(commands=['vpn_get'])
    def handle(message):
        if (user_verification(message.from_user.id) == True):
            bot.reply_to(
                message, "enter the name of the peer you want the information of (type No to abort)")
            bot.register_next_step_handler(message, step2_vpn_get)

    def step2_vpn_get(message):
        if (user_verification(message.from_user.id) == True):
            if message.text in nos:
                bot.reply_to(message, "Operation aborted")
            else:
                result = subprocess.run(
                    ["python3", "vpn.py", "get", message.text], capture_output=True, text=True)
                caption = result.stdout
                result = subprocess.run(
                    ["python3", "vpn.py", "get_image", message.text], capture_output=True, text=True)
                tmp = result.stdout.replace("\n", "")
                with open(tmp, "rb") as image:
                    bot.send_photo(USER_ID, image, caption=caption,
                                   parse_mode="Markdown")
                image.close()
##############################################
##              SSH ACTIONS                 ##
##############################################

    @bot.message_handler(commands=['ssh_up'])
    def handle(message):
        if (user_verification(message.from_user.id) == True):
            result = subprocess.run(
                ["python3", "ssh.py", "up"], capture_output=True, text=True)
            bot.reply_to(message, result.stdout)

    @bot.message_handler(commands=['ssh_down'])
    def handle(message):
        if (user_verification(message.from_user.id) == True):
            result = subprocess.run(
                ["python3", "ssh.py", "down"], capture_output=True, text=True)
            bot.reply_to(message, result.stdout)

    @bot.message_handler(commands=['ssh_status'])
    def handle(message):
        if (user_verification(message.from_user.id) == True):
            result = subprocess.run(
                ["python3", "ssh.py", "status"], capture_output=True, text=True)
            bot.reply_to(message, result.stdout)

    @bot.message_handler(commands=['ssh_info'])
    def handle(message):
        if (user_verification(message.from_user.id) == True):
            result = subprocess.run(
                ["python3", "ssh.py", "info"], capture_output=True, text=True)
            bot.reply_to(message, result.stdout, parse_mode='Markdown')

    @bot.message_handler(commands=['ssh_add'])
    def handle(message):
        if (user_verification(message.from_user.id) == True):
            bot.reply_to(
                message, "Paste the public key found by doing \n`cat ~/.ssh/raspberry.pub`\n or write <No> to abort", parse_mode='Markdown')
            bot.register_next_step_handler(message, step2)

    def step2(message):
        if (user_verification(message.from_user.id) == True):
            nos = ["no", "nO", "No", "NO"]
            if message.text in nos:
                bot.reply_to(message, "Operation aborted")
            else:
                result = subprocess.run(
                    ["python3", "ssh.py", "add", message.text], capture_output=True, text=True)
                bot.reply_to(message, result.stdout)

##############################################
##              MISC ACTIONS                ##
##############################################
    @bot.message_handler(commands=['update'])
    def handle(message):
        if (user_verification(message.from_user.id) == True):
            result = subprocess.run(
                ["python3", "misc.py", "update"],
                capture_output=True,
                text=True
            )
            bot.reply_to(message,  result.stdout)

    @bot.message_handler(commands=['reboot'])
    def handle(message):
        if (user_verification(message.from_user.id) == True):
            subprocess.run(["python3", "misc.py", "reboot"])

    bot.infinity_polling()
