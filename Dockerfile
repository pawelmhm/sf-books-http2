FROM ubuntu:16.04

RUN apt-get update
RUN apt-get install -y python3 python3-dev python3-pip build-essential libssl-dev libffi-dev nginx vim

WORKDIR /app
ADD requirements.txt /app

RUN pip3 install -r requirements.txt
COPY conf /etc/nginx/sites-available/default

CMD python3 server.py
