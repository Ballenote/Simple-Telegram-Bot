import subprocess
import sys


def update():
    result = subprocess.run(
        ["sh", "/home/casa/Documents/bot_updater.sh", "0"],
        capture_output=True,
        text=True
    )
    if (result.returncode == 0):
        return (result.stdout)

    else:
        return (result.stderr)


def reboot():
    subprocess.run(["sudo", "reboot"])


if __name__ == "__main__":

    output = "If you see this there was an error in the code"

    match sys.argv[1]:
        case "update":
            output = update()
        case "reboot":
            reboot()

    print(output)
