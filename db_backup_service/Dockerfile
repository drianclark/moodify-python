FROM golang:alpine

COPY . /app
WORKDIR /app

RUN apk add --no-cache git

RUN go get github.com/imroc/req

ENTRYPOINT [ "/bin/sh" ]

CMD [ "backupService.sh" ]
