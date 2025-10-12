import subprocess
import sys
import os
from dotenv import load_dotenv


def vpn_action(action):
    #Actually turning on or off the Wireguard instance
    result = subprocess.run(
        ["sudo", 'wg-quick', action, 'wg0'],
        capture_output=True,
        text=True
    )
    if (result.returncode == 0):
        if(sys.argv[1]=="up"):
            output="The VPN is now active."
        else:
            output="The VPN is now deactivated."
    else:
        output= result.stderr
    return output

def vpn_info():
    #Gathering useful info for Wireguard

    load_dotenv("secrets.env")
    PUB_KEY = os.getenv("PUB_KEY")
    PORT = os.getenv("VPN_PORT")
    pubipv6 =  subprocess.run(
            ["curl","https://ifconfig.me/"],
            capture_output=True,
            text=True
            ).stdout
    pubipv4 = subprocess.run(
            ["curl","-4","https://ifconfig.me/"],
            capture_output=True,
            text=True
            ).stdout
    return f"The public IPV6 and V4 are: \n\n`{pubipv6}`\n\n`{pubipv4}`\n\nThe WireGuard port is \n\n`{PORT}`\n\nThe public key of the server is \n\n`{PUB_KEY}`\n"

if __name__== "__main__":
    
    output="If you see this there was an error in the code"

    match sys.argv[1]:
        case "up":      
            output=vpn_action("up")
        case "down":
            output=vpn_action("down")
        case "info":
            output=vpn_info() 

    

    print(output)