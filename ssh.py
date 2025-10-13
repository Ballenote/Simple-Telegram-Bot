import subprocess
import os
import sys
from dotenv import load_dotenv


def ssh_action(action):
    result = subprocess.run(
        ["sudo", 'systemctl', action, 'ssh.service'],
        capture_output=True,
        text=True,
        check=False
    )
    if (action == "stop"):
        result2 = subprocess.run(
            ["sudo", 'systemctl', action, 'ssh.socket'],
            capture_output=True,
            text=True,
            check=False
        )

    if result.returncode == 0:
        if action == "stop":
            if result2.returncode == 0:
                return "The SSH connection is deactivated"
            else:
                return result2.stderr
        else:
            return "The SSH connection is activated"
    else:
        return result.stderr


def ssh_status():
    p1 = subprocess.Popen(["sudo", "systemctl", "status",
                          "ssh"], stdout=subprocess.PIPE)
    p2 = subprocess.Popen(["grep", "Active"],
                          stdin=p1.stdout, stdout=subprocess.PIPE)
    p1.stdout.close()
    output, error = p2.communicate()
    return output.decode()


def ssh_info():
    load_dotenv("secrets.env")
    PORT = os.getenv("SSH_PORT")
    IP = os.getenv("LOCAL_IP")
    line = f"To connect to the machine, first connect through Wireguard and then run:\n\n`ssh -i ~/.ssh/raspberry -p {PORT} casa@{IP}`\n"
    return line


def ssh_add(cert):
    with open("/home/casa/.ssh/authorised_keys", "a") as f:
        f.write(cert)
    f.close()
    return "Certificate added."


if __name__ == "__main__":

    output = "If you see this there was an error in the code"

    match sys.argv[1]:
        case "up":
            output = ssh_action("start")
        case "down":
            output = ssh_action("stop")
        case "status":
            output = ssh_status()
        case "info":
            output = ssh_info()
        case "add":
            output = ssh_add(sys.argv[2])

    print(output)
