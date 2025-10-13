import subprocess
import sys
import os
from dotenv import load_dotenv
import io
import base64

path = "/home/casa/Documents/Wireguard_Peers"


def load_peers():
    loaded = []
    path = "/home/casa/Documents/Wireguard_Peers"
    for peer in sorted(os.listdir(path)):
        for conf in os.listdir(f"{path}/{peer}"):
            if conf == f"server.conf":
                print(peer)
                with open(f"{path}/{peer}/{conf}") as f:
                    lines = f.read()
                f.close()
                info = lines.split()
                print(info)
                result = subprocess.run(
                    ["sudo", "wg", "set", "wg0", "peer", info[0], "allowed-ips", info[1], "preshared-key", info[2]], capture_output=True, text=True)
                if (result.returncode == 0):
                    loaded.append(peer)
                else:
                    loaded.append(result.stderr)
    return loaded


def vpn_action(action):
    # Actually turning on or off the Wireguard instance
    result = subprocess.run(
        ["sudo", 'wg-quick', action, 'wg0'],
        capture_output=True,
        text=True
    )
    if (result.returncode == 0):
        if (sys.argv[1] == "up"):
            output = "The VPN is now active."
            loaded = load_peers()
            output = output+"\n peers loaded:\n"
            for element in loaded:
                output = output+f"{element}\n"
        else:
            output = "The VPN is now deactivated."
    else:
        output = result.stderr
    return output


def vpn_info(special):
    # Gathering useful info for Wireguard

    load_dotenv("secrets.env")
    PUB_KEY = os.getenv("PUB_KEY")
    PORT = os.getenv("VPN_PORT")
    pubipv6 = subprocess.run(
        ["curl", "https://ifconfig.me/"],
        capture_output=True,
        text=True
    ).stdout
    pubipv4 = subprocess.run(
        ["curl", "-4", "https://ifconfig.me/"],
        capture_output=True,
        text=True
    ).stdout
    if (special == True):
        return [pubipv4, PORT, PUB_KEY]
    else:
        return f"The public IPV6 and V4 are: \n\n`{pubipv6}`\n\n`{pubipv4}`\n\nThe WireGuard port is \n\n`{PORT}`\n\nThe public key of the server is \n\n`{PUB_KEY}`\n"


def vpn_status():
    result = subprocess.run(
        ["sudo", 'wg', 'show'],
        capture_output=True,
        text=True
    )
    if (len(result.stdout) > 0):
        return "the VPN connection is active"
    else:
        return "the VPN connection is not active"


def vpn_list():
    output = ""
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)
    for peer in os.listdir(path):
        output = output+"`"+peer+"`\n"
    if output == "":
        output = "Nothing to show"
    return output


def peer_find(name):
    found = False
    latest = 1
    name = name.strip().lower()
    for peer in sorted(os.listdir(path)):
        tmp = peer.split("_")
        latest = int(tmp[0])
        if (name == tmp[1]):
            found = True
            break
    return found, latest


def vpn_create(newPeer):
    output = "if you see this there was a problem"
    newPeer = newPeer.strip().lower()
    found, latest = peer_find(newPeer)

    if (found == True):
        output = f"The peer already exists with ID {latest}"
    else:
        info = vpn_info(True)
        result = subprocess.run(["bash", "/home/casa/Documents/Simple-Telegram-Bot/vpn_creator.sh", str(path), str(latest+1), str(
            newPeer.strip().lower()), str(info[0]), str(info[1]), str(info[2])], capture_output=True, text=True)
        if (result.returncode == 0):
            output = "To be pasted in the wg0.conf file in the machine:"
        else:
            output = result.stderr

    return output


def vpn_get(name):
    output = "if you see this there was a problem"
    name = name.strip().lower()
    found, id = peer_find(name)

    if not found:
        output = f"Unable to locate {name}"
    else:
        dir = f"{path}/{id}_{name}"
        result = subprocess.run(
            ["cat", f"{dir}/{name}.conf"], capture_output=True, text=True)
        output = f"`{result.stdout}`"
    return output


def vpn_get_image(name):
    output = "if you see this there was a problem"
    name = name.strip().lower()
    found, id = peer_find(name)

    if not found:
        output = f"Unable to locate {name}"
    else:
        dir = f"{path}/{id}_{name}"
        output = f"{dir}/{name}-qr.png"
    return output


if __name__ == "__main__":

    output = "If you see this there was an error in the code"

    match sys.argv[1]:
        case "up":
            output = vpn_action("up")
        case "down":
            output = vpn_action("down")
        case "info":
            output = vpn_info(False)
        case "status":
            output = vpn_status()
        case "list":
            output = vpn_list()
        case "create":
            output = vpn_create(sys.argv[2])
        case "get":
            output = vpn_get(sys.argv[2])
        case "get_image":
            output = vpn_get_image(sys.argv[2])

    print(output)
