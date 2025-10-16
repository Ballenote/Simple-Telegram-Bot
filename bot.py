from dotenv import load_dotenv
import telebot
import os
import subprocess

output = "if you see this there was a problem in the code"
options = ["up", "down", "info", "status", "list"]
twosetp = ["add", "get", "create"]
misc = ["update", "reboot", "start"]
functions = ["vpn", "ssh"]
nos = ["no", "nO", "No", "NO"]

# loading secrets
load_dotenv("secrets.env")
BOT_TOKEN = os.getenv("BOT_TOKEN")
USER_ID = os.getenv("USER_ID")


def user_verification(uuid):
    # only my user ID can use the bot
    if uuid == (int(USER_ID)):
        return True


def step2(message, command, action):

    if message.text in nos:
        bot.reply_to(message, "Operation aborted")
    else:
        # running the second command after the user input
        result = subprocess.run(
            ["python3", f"{action}.py", command, message.text],
            capture_output=True,
            text=True,
        )

        if result.returncode == 0:
            # extra command to load the qr code for vpn peers
            if command in ["get", "create"]:
                caption = result.stdout
                result = subprocess.run(
                    ["python3", "vpn.py", "get_image", message.text],
                    capture_output=True,
                    text=True,
                )
                result.stdout = eval(result.stdout)

                if result.stdout[0] is True:
                    # if false the folder of the peer was not found
                    with open(result.stdout[1], "rb") as image:
                        bot.send_photo(
                            USER_ID, image, caption=caption, parse_mode="Markdown"
                        )
                    image.close()
                else:
                    # sending the user not found error
                    bot.reply_to(message, result.stdout[1])
            else:
                # sending the info for messages not requiring and extra step
                bot.reply_to(message, result.stdout)
        else:
            # sending the error in case of problems with calling the other script
            bot.reply_to(message, "There was an error in performing the action (step2)")


def handle(command):
    present = False
    extrastep = False
    output = "This command is not implemented"
    action = ""

    if command[:3] in functions:
        # evaluating the type of action in either ssh or vpn commands
        action = command[:3]
        command = command[4:]

        if command in options:
            # only 1 answer commands
            present = True

        if command in twosetp:
            # commands where the user has to type something
            present = True
            extrastep = True

            match command:
                case "add":
                    output = "Paste the public key found by doing \n`cat ~/.ssh/raspberry.pub`\n (type No to abort)"
                case "get":
                    output = "Enter the name of the peer you want the information of (type No to abort)"
                case "create":
                    output = "Enter the name of the peer you want to create (type No to abort)"

    if command in misc:
        # non ssh or vpn commands
        present = True
        action = "misc"

    return present, extrastep, output, action, command


if __name__ == "__main__":
    # Where most of the bot interface is

    bot = telebot.TeleBot(BOT_TOKEN)

    bot.send_message(USER_ID, "The bot is back online.")

    @bot.message_handler()
    def universal_handler(message):

        if user_verification(message.from_user.id) == True:
            command = message.text

            if command[0] == "/":
                # only considering commands and not text
                present, extrastep, output, action, command = handle(command[1:])

                if present == True and extrastep == False:
                    # processing commands that require only 1 interaction
                    result = subprocess.run(
                        ["python3", f"{action}.py", command],
                        capture_output=True,
                        text=True,
                    )
                    
                    if result.returncode == 0:
                        output = result.stdout
                    else:
                        output = "There was an error in running the command (universal_handler)"

                bot.reply_to(message, output, parse_mode="Markdown")

                if extrastep == True:
                    # handling 2 step interactions (waiting for user input)
                    bot.register_next_step_handler(message, step2, command, action)

    bot.infinity_polling()
