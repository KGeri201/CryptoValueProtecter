FROM python:latest

RUN apt-get update -y && apt-get upgrade -y

RUN apt-get install nginx -y

COPY index.html /var/www/html/

WORKDIR /usr/src/app

COPY . /usr/src/app/

RUN pip3 install --no-cache-dir -r /usr/src/app/requirements.txt

EXPOSE 80/tcp

VOLUME ["/usr/src/app"]

CMD ["python3", "./CryptoBot.py"]
