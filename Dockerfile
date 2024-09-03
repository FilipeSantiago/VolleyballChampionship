FROM python:3.10.14
MAINTAINER Filipe Santiago <ftsantiago95@gmail.com>

ARG APP_PORT
ARG ORS_ENDPOINT
ARG DATABASE_SERVICE
ARG DATABASE_HOST
ARG DATABASE_PORT
ARG DATABASE_NAME
ARG DATABASE_SCHEMA
ARG db_user
ARG db_pass

ENV APP_PORT=5000
ENV DATABASE_SERVICE=postgresql
ENV DATABASE_HOST=volley.czuqgkag2bmh.sa-east-1.rds.amazonaws.com
ENV DATABASE_PORT=5432
ENV DATABASE_NAME=volley_championship
ENV DATABASE_SCHEMA=public
ENV DATABASE_USER=$db_user
ENV DATABASE_PASSWORD=$db_pass

ENV PYTHONPATH=/app

RUN pip install --upgrade pip

WORKDIR /app
COPY . /app

RUN pip install uwsgi
RUN pip --no-cache-dir install -r requirements.txt

EXPOSE 5000 0
CMD ["uwsgi", "--ini", "/app/wsgi.ini"]
