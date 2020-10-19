FROM python:3.9-rc-slim-buster

COPY . /app
WORKDIR /app
RUN pip3 install -r requirements.txt

ENTRYPOINT [ "python3" ]

CMD [ "tracks_service.py" ]
