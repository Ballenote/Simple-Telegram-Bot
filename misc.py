import subprocess
import sys

output = "If you see this there was an error in the code"


def update():
    # Checking for updates in the code
    result = subprocess.run(
        ["sh", "/home/casa/Documents/Simple-Telegram-Bot/bot_updater.sh", "0"],
        capture_output=True,
        text=True,
    )
    if result.returncode == 0:
        output="Updates downloaded"
    else:
        return result.stderr

    return output


def reboot():
    # Rebooting the system
    subprocess.run(["sudo", "reboot"])
    return "rebooting"


if __name__ == "__main__":

    match sys.argv[1]:
        case "update":
            output = update()
        case "reboot":
            output=reboot()
        case "start":
            output = "Welcome!"
        case _:
            output = "Command not found."

    print(output)
