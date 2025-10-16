import subprocess
import sys
import os
from dotenv import load_dotenv

path = "/home/casa/Documents/Wireguard_Peers"
output = "if you see this there was a problem"


def load_peers():
    # Loading the configuration of each peer after the server has started
    loaded = []

    for peer in sorted(os.listdir(path)):
        for conf in os.listdir(f"{path}/{peer}"):
            if conf == "server.conf":

                with open(f"{path}/{peer}/{conf}", "r") as f:
                    lines = f.read()
                f.close()

                info = lines.split()
                result = subprocess.run(
                    [
                        "sudo",
                        "wg",
                        "set",
                        "wg0",
                        "peer",
                        info[0],
                        "allowed-ips",
                        info[1],
                        "preshared-key",
                        info[2],
                    ],
                    capture_output=True,
                    text=True,
                )

                if result.returncode == 0:
                    loaded.append(peer[1:])
                else:
                    loaded.append(result.stderr)

    return loaded


def vpn_action(action):
    # Turning on and off the Wireguard instance
    result = subprocess.run(
        ["sudo", "wg-quick", action, "wg0"], capture_output=True, text=True
    )

    if result.returncode == 0:
        if action == "up":
            
            output = "The VPN is now active.\nPeers loaded:"

            loaded = load_peers()
            for element in loaded:
                output = output + f"\n{element[1:]}"

    else:
        output = vpn_status()

    return output


def vpn_info(special):
    # Gathering useful info for Wireguard clients

    load_dotenv("secrets.env")
    PUB_KEY = os.getenv("PUB_KEY")
    PORT = os.getenv("VPN_PORT")

    pubipv6 = subprocess.run(
        ["curl", "https://ifconfig.me/"], capture_output=True, text=True
    ).stdout

    pubipv4 = subprocess.run(
        ["curl", "-4", "https://ifconfig.me/"], capture_output=True, text=True
    ).stdout

    if special is True:
        # Providing info in a different format
        output = [pubipv4, PORT, PUB_KEY]
    else:
        output = f"The public IPV6 and IPV4 are: \n\n`{pubipv6}`\n\n`{pubipv4}`\n\nThe WireGuard port is \n\n`{PORT}`\n\nThe public key of the server is \n\n`{PUB_KEY}`\n"

    return output


def vpn_status():
    # Shows the status of the Wireguard interface on the server
    result = subprocess.run(["sudo", "wg", "show"], capture_output=True, text=True)
    if len(result.stdout) > 0:
        output = "the VPN connection is active"
    else:
        output = "the VPN connection is not active"

    return output


def vpn_list():
    # Lists all the peers that the VPN provides a connection to
    output = ""
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)

    for peer in os.listdir(path):
        output = output + "`" + peer[2:] + "`\n"
    if output == "":
        output = "Nothing to show"

    return output


def peer_find(name):
    # finds if a peer is present in the configuration
    found = False
    latest = 1

    for peer in sorted(os.listdir(path)):
        tmp = peer.split("_")
        latest = int(tmp[0])
        if name == tmp[1]:
            found = True
            break

    return found, latest


def vpn_create(newPeer):
    # Creates a new peer
    found, latest = peer_find(newPeer)

    if found is True:
        output = vpn_get(newPeer)
    else:
        info = vpn_info(True)
        result = subprocess.run(
            [
                "bash",
                "/home/casa/Documents/telegram-bot/vpn_creator.sh",
                str(path),
                str(latest + 1),
                str(newPeer.strip().lower()),
                str(info[0]),
                str(info[1]),
                str(info[2]),
            ],
            capture_output=True,
            text=True,
        )
        if result.returncode == 0:
            output = vpn_get(newPeer)
        else:
            output = result.stderr

    return output


def vpn_get(name):
    found, id = peer_find(name)
    if not found:
        output = f"Unable to locate {name}"
    else:
        dir = f"{path}/{id}_{name}"
        result = subprocess.run(
            ["cat", f"{dir}/{name}.conf"], capture_output=True, text=True
        )
        output = f"`{result.stdout}`"

    return output


def vpn_get_image(name):
    found, id = peer_find(name)

    if not found:
        output = f"Unable to locate {name}"
    else:
        dir = f"{path}/{id}_{name}"
        output = f"{dir}/{name}-qr.png"

    return [found, output]


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
            output = vpn_create(sys.argv[2].strip().lower())
        case "get":
            output = vpn_get(sys.argv[2].strip().lower())
        case "get_image":
            output = vpn_get_image(sys.argv[2].strip().lower())

    print(output)
