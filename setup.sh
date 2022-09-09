#!/bin/bash

sudo apt-get install python3 -y

#sudo apt-get install nginx -y

pip3 install --no-cache-dir -r requirements.txt

#sudo cp index.html /var/www/html/

sed -i "s|path|$PWD|g" cryptobot.service

sudo cp cryptobot.service /etc/systemd/system/
