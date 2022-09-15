FROM python:latest

RUN apt-get update -y && apt-get upgrade -y

RUN apt-get install wget -y

WORKDIR /usr/src/app

RUN wget -P /usr/src/app/ https://raw.githubusercontent.com/KGeri201/CryptoValueProtecter/main/setup.sh | bash

EXPOSE 80/tcp

VOLUME ["/usr/src/app"]

CMD ["python3", "./CryptoBot.py"]
