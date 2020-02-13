FROM python:3.6-stretch

ENV PYTHONUNBUFFERED 1
ENV DOCKER_CONTAINER 1

RUN apt update && apt upgrade -y

COPY ./requirements/common.txt /opt/mes-cloud/common.txt
COPY ./requirements/prod.txt /opt/mes-cloud/prod.txt
RUN pip install -r /opt/mes-cloud/prod.txt

COPY . /opt/mes-cloud
WORKDIR /opt/mes-cloud

EXPOSE 8001
