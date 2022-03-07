FROM python:3.9

WORKDIR /usr/src/app/

ENV PYTHONDONTWRITEBYTECODE 1

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt ./

RUN pip install -r requirements.txt

COPY . .