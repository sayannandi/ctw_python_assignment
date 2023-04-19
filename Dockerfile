FROM python:3.11.3-alpine

RUN apk add --update --no-cache gcc libc-dev libffi-dev

WORKDIR /srv

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY ./src ./src

ENV PYTHONPATH=/srv/src

RUN pip3 install --upgrade pip
