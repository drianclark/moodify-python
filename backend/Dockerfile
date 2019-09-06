FROM ubuntu:18.04

MAINTAINER Adrian David "dreiclark@gmail.com"

RUN apt-get update -y && apt-get install -y python3-pip python3-dev libmysqlclient-dev

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip3 install -r requirements.txt
RUN pip3 install -U flask-cors

COPY . /app

ENTRYPOINT [ "python3" ]

CMD [ "app/tracks_service.py" ]
