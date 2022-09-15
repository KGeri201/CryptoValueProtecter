<img src="CryptoValueProtecter.svg" alt="Crypto Value Protecter" height="200"/>  

# CVP
**C**rypto **V**alue **P**rotecter

## Description
It is a bot written in python, which monitors your binance crypto wallet in custom intervalls
and automatically trades your crypto currencies and tokens 
when their price change percentage changes under a custom threshold.  
It will also have an easy to read web UI to easily monitor the bot from everywhere.

## Installation
### Bare metal
Make sure you have wget installed to download and execute the setup script as sudo
```
wget https://raw.githubusercontent.com/KGeri201/CryptoValueProtecter/main/setup.sh | bash
```
It will install python3
```
apt-get install python3 -y
```
download all the needed files
```
wget https://raw.githubusercontent.com/KGeri201/CryptoValueProtecter/main/CryptoBot.py
wget https://raw.githubusercontent.com/KGeri201/CryptoValueProtecter/main/requirements.txt
wget -P /var/www/html/ https://raw.githubusercontent.com/KGeri201/CryptoValueProtecter/main/index.html
wget -P /etc/systemd/system/ https://raw.githubusercontent.com/KGeri201/CryptoValueProtecter/main/cryptobot.service
```
and add the path of the bot into the service file.
```
sed -i "s|path|$PWD|g" /etc/systemd/system/cryptobot.service
```
It wills also install all the needed python requirements.
```
pip3 install --no-cache-dir -r requirements.txt
```

### Docker
#### Easy and fast
Quick install with docker run:  
Clone/download the project onto your local machine and execute
```
docker run -it --rm --name cryptobot -v "$PWD":/usr/src/app -w /usr/src/app python python3 CryptoBot.py
```
You will also have to create the config.yaml as described under "Usage" and install all the needed python library requirements
#### Custom container
For that it is enough to download the Dockerfile and optionally the docker-compose.yaml, if you want to use docker-compose.
```
wget https://raw.githubusercontent.com/KGeri201/CryptoValueProtecter/main/Dockerfile
```
```
wget https://raw.githubusercontent.com/KGeri201/CryptoValueProtecter/main/docker-compose.yaml
```

## Usage
Create a file called config.yaml in and place it inside the working directory of your container or right next to the CryptoBot.py.
```
api_key: "<API_KEY>"
api_secret: "<API_SECRET>"

currency: "EUR"

time_to_wait: 24
time_unit: "hour"

trade_threshold: 0

doomsdaymeasures: False

monitor = False

logging_level: 2
debug: False
```
### Start it as a service
```
sudo systemctl start cryptobot.service
```
or just start the python script directly, by going into the main folder of the project and executing 
```
python3 CryptoBot.py
```
The service file also can be enabled to automatically start by booting the computer
```
sudo systemctl enable cryptobot.service
```
### Start it as a container
#### Use docker-compose
docker-compose.yaml:
```
version: '3.3'
services:
    cryptobot:
        build: .
        container_name: cryptobot
        restart: always
        volumes:
            - $PWD:/usr/src/app
        working_dir: 
            - /usr/src/app
```
Start the container by executing:
```
docker-compose up -d
```
#### Build it manually
Build the container.
```
docker build -t cryptobot .
```
Start the container.
```
docker run -it --rm --name -v $PWD:/usr/src/app cryptobot cryptobot
```

## Credits
[KGeri201](https://github.com/KGeri201)

## License
[GNU GENERAL PUBLIC LICENSE](LICENSE)

## Project status
In development.
