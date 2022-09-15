#!/bin/bash

sudo apt-get install wget python3 -y

#sudo apt-get install nginx -y

sudo wget https://raw.githubusercontent.com/KGeri201/CryptoValueProtecter/main/LICENSE
sudo wget https://raw.githubusercontent.com/KGeri201/CryptoValueProtecter/main/README.md
sudo wget https://raw.githubusercontent.com/KGeri201/CryptoValueProtecter/main/CryptoBot.py
sudo wget https://raw.githubusercontent.com/KGeri201/CryptoValueProtecter/main/requirements.txt
sudo wget -P /var/www/html/ https://raw.githubusercontent.com/KGeri201/CryptoValueProtecter/main/index.html
sudo wget -P /etc/systemd/system/ https://raw.githubusercontent.com/KGeri201/CryptoValueProtecter/main/cryptobot.service

sudo pip3 install --no-cache-dir -r requirements.txt

sudo sed -i "s|path|$PWD|g" /etc/systemd/system/cryptobot.service
