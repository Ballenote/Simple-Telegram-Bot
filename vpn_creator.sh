#!/bin/sh

dir="$1"
id="$2"
peer="$3"
ip="$4"
port="$5"
pubk="$6"

path="$dir"/"$id"_"$peer"

mkdir $path
cd $path

wg genkey | tee "$peer.key" | wg pubkey > "$peer-pub.key"
wg genpsk > "$peer-psk.key"

#creation of client configuration
client="$peer".conf
echo "[Interface]">$client
echo "PrivateKey = $(cat $peer.key)" >> $client
echo "Address = 10.0.0.$id/32" >> $client
echo >>$client
echo "[Peer]">>$client
echo "PublicKey = $pubk">>$client
echo "PresharedKey = $(cat $peer-psk.key)">>$client
echo "Endpoint = $ip:$port" >> $client
echo "AllowedIPs = 0.0.0.0/0,10.0.0.0/32" >> $client
echo "PersistentKeepalive = 25" >>$client

#Geneating server config
echo "$(cat $peer-pub.key)">>"server.conf"
echo "10.0.0.$id/32" >> "server.conf"
echo "$path/$peer-psk.key" >> "server.conf"

#generating QR
qrencode -o "$peer-qr.png" < "$peer.conf"
exit 0