import subprocess
import os
import sys
from dotenv import load_dotenv

output = "If you see this there was an error in the code"


def ssh_action(action):
    # Starting or stopping the SSH server
    result = subprocess.run(
        ["sudo", "systemctl", action, "ssh.service"],
        capture_output=True,
        text=True,
        check=False,
    )

    if action == "stop":
        # stopping the ssh server also requires stopping its socket
        result2 = subprocess.run(
            ["sudo", "systemctl", action, "ssh.socket"], capture_output=True, text=True
        )

    if result.returncode == 0:
        if action == "stop":
            if result2.returncode == 0:
                output = "The SSH connection is deactivated"
            else:
                output = result2.stderr
        else:
            output = "The SSH connection is activated"
    else:
        output = result.stderr

    return output


def ssh_status():
    # Checks the status of the SSH server
    p1 = subprocess.Popen(
        ["sudo", "systemctl", "status", "ssh"], stdout=subprocess.PIPE
    )
    p2 = subprocess.Popen(["grep", "Active"], stdin=p1.stdout, stdout=subprocess.PIPE)
    p1.stdout.close()
    output, error = p2.communicate()

    return output.decode()


def ssh_info():
    # Gets useful info to connect to the SSH server
    load_dotenv("secrets.env")
    PORT = os.getenv("SSH_PORT")
    IP = os.getenv("LOCAL_IP")
    output = f"To connect to the machine, first connect through Wireguard and then run:\n\n`ssh -i ~/.ssh/raspberry -p {PORT} casa@{IP}`\n"

    return output


def ssh_add(cert):
    # Adds and authorised key to connect
    with open("/home/casa/.ssh/authorised_keys", "a") as f:
        f.write(cert)
    f.close()

    return "Certificate added."


if __name__ == "__main__":

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
