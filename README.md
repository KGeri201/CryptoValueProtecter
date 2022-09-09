<img src="CryptoValueProtecter.svg" alt="Crypto Value Protecter" height="200"/>  

# CVP
**C**rypto **V**alue **P**rotecter

## Description
It is a bot written in python, which monitors your binance crypto wallet in custom intervalls
and automatically trades your crypto currencies and tokens 
when their price change percentage changes under a custom threshold.  
It will also have an easy to read web UI to easily monitor the bot from everywhere.

## Installation
Clone/copy the project. 
Create a file called config.yaml in the main directory of the project.
```
api_key: "<API_KEY>"
api_secret: "<API_SECRET>"

currency: "EUR"

time_to_wait: 24
time_unit: "hour"

trade_threshold: 0

doomsdaymeasures: False

start_website: False

logging_level: 2
debug: False
```
Then choose one of the two methods:
### Bare metal
Go into the main directory of the project and execute the setup script
```
.\setup.sh
```
It will install python3, nginx and all the needed requirements.
```
sudo apt-get install python3 nginx -y
```
```
pip3 install --no-cache-dir -r requirements.txt
```
It will copy the index.html to the /var/www/html/ folder and replace the default html file.
```
sudo cp index.html /var/www/html/
```
Adds the path of the bot into the service file
```
sed -i "s|CryptoBot.py|$PWD/CryptoBot.py|g" cryptobot.service
```
and copies it.
```
sudo cp cryptobot.service /etc/systemd/system/
```
#### Start
Start the service
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
### Docker
#### Easy and fast
Quick install with docker run:
```
docker run -it --rm --name cryptobot -v "$PWD":/usr/src/app -w /usr/src/app python python3 CryptoBot.py
```
#### Custom container
##### Use docker-compose
docker-compose.yaml in the main directory of the project:
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
##### Do it manually
Build the container.
```
docker build -t cryptobot .
```
Start the container.
```
docker run -it --rm --name cryptobot cryptobot
```

## Credits
[KGeri201](https://github.com/KGeri201)

## License
[GNU GENERAL PUBLIC LICENSE](LICENSE)

## Project status
In development.
