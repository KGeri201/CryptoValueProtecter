#!/bin/bash

apt-get install python3 -y

#sudo apt-get install nginx -y

wget https://raw.githubusercontent.com/KGeri201/CryptoValueProtecter/main/LICENSE
wget https://raw.githubusercontent.com/KGeri201/CryptoValueProtecter/main/README.md
wget https://raw.githubusercontent.com/KGeri201/CryptoValueProtecter/main/CryptoBot.py
wget https://raw.githubusercontent.com/KGeri201/CryptoValueProtecter/main/requirements.txt
wget -P /var/www/html/ https://raw.githubusercontent.com/KGeri201/CryptoValueProtecter/main/index.html
wget -P /etc/systemd/system/ https://raw.githubusercontent.com/KGeri201/CryptoValueProtecter/main/cryptobot.service

sed -i "s|path|$PWD|g" /etc/systemd/system/cryptobot.service

pip3 install --no-cache-dir -r requirements.txt
