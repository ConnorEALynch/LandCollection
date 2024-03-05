# syntax=docker/dockerfile:1.4

#https://github.com/docker/awesome-compose/tree/master/django

FROM --platform=$BUILDPLATFORM python:3.12-alpine AS builder
EXPOSE 8000/tcp



WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

#node/webpack
COPY ./package.json ./package-lock.json /app/
COPY ./webpack.config.js /app
RUN apk add --update npm
RUN npm install


RUN npm run prod
COPY . /app/

#python/django
COPY requirements.txt /app
RUN pip3 install -r requirements.txt --no-cache-dir




COPY ./entrypoint.sh /app/entrypoint.sh
RUN chmod 755 ./entrypoint.sh
ENTRYPOINT [ "./entrypoint.sh" ]