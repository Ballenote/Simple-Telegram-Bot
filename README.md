# Simple-Telegram-Bot


This project runs a telegram bot that has the following features:

 #### VPN through Wireguard
 1. Turn the VPN interface `up` and `down`
 2. Get the `status` of the interface and useful `info` to connect to it
 3. Get information about the `list` of current peers
 4. `create` the configuration of new peers, both in a .conf file and QR code
 5. `get` the configuration of an existing peer
 
 #### SSH connection after connecting to the VPN
 1. Turn the SSH interface `up` and `down`
 2. Get the `status` of the interface and useful `info` to connect to it
 3. `add` a new certificate to the list of trusted peers

 #### Misc
1. Check for an `update` in the git repository and download it
2. `reboot` the machine

BEAR IN MIND THAT THIS BOT WILL ONLY WORK BY SPECIFYING YOUR TELEGRAM USER ID.

## Installation
### Creating the bot in Telegram
1. Create a new bot in `BotFather`
2. Copy the API key for later use
3. Add the following commands:
```
/vpn_up
/vpn_down
/vpn_list
/vpn_info
/vpn_status
/vpn_create
/vpn_get
/ssh_up
/ssh_down
/ssh_status
/ssh_add
/update
/reboot
```

### Cloning the repository 
1. Install Git by running `sudo apt-get install git-all`
2. In `Documents` run `git clone https://github.com/Ballenote/Simple-Telegram-Bot.git`

### Wireguard
 1. Install Wireguard and SSH server: `sudo apt install -y wireguard`
 2. Generate the public and private key of the server: `cd /etc/wireguard && umask 077 && wg genkey | tee server_private.key | wg pubkey > server_public.key`
3. Create the configuration of the Wireguard interface: `sudo nano /etc/wireguard/wg0.conf`
4. Add the values of the private key and prot in the configuration of step 3:
```
[Interface]
Address = 10.0.0.1/32
SaveConfig = false
PostUp = iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE; ip route add 10>
PostDown = iptables -t nat -D POSTROUTING -o eth0 -j MASQUERADE; ip route del >
ListenPort = <Choose a port>
PrivateKey = <The private key>
```
5. Change the permissions on the key files: `sudo chmod 600 /etc/wireguard/server_private.key /etc/wireguard/wg0.conf`
6. Open the port in the router to allow the redirection of the traffic to the host

### SSH Server
1. Install the SSH server: `sudo apt install -y openssh-server`
2. Make a configuration file of the SSH server: `nano /etc/ssh/sshd_config.d/ssh.conf` and paste the following information:
```
Port <Specify a port>
Protocol 2
PermitRootLogin no
PasswordAuthentication no
ChallengeResponseAuthentication no
KbdInteractiveAuthentication no
UsePAM no
PubkeyAuthentication yes
PermitUserEnvironment no
AllowAgentForwarding no
AllowTcpForwarding yes  
LogLevel VERBOSE
PubkeyAuthentication yes
AuthorizedKeysFile /home/<your user>/.ssh/authorised_keys
```
3. Create the authorised_keys file: `touch ~/.ssh/authorised_keys`

To generate a key in the client and later push it to the bot in the autorised keys run: `ssh-keygen -t raspberry -C "<Yout identity>"` 

### Automated execution of the bot
1. Create a sudoers file for the commands that will be used by the bot: `sudo visudo /etc/sudoers.d/telegram-bot ` and paste the contents of the `sudoers.txt` file in the repository
2. Create a crontab to allow periodic installation of updates and the automated execution at reboot of the script: `crontab -e` and paste the content of `crontab.txt`
3. In the folder of the repository, create a `secrets.env` file,  paste the contents of the `secrets.txt` file and write the required information so the program can run properly.
4. In the folder of the repository create a python virtual environment in the repository folder using: `python3 -m venv myenv`
5. Activate the environment by running `source .venv/bin/activate`
6. Run `pip install telebot dotenv`

### Running the bot
You can either reboot the system or launch the bot
**You will generally have to check that the user in some paths corresponds to the user in your machine!**

