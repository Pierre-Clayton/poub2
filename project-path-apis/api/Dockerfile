# nginx-gunicorn-flask

FROM python:3.12
LABEL maintainer "Elvis Bando <elvisbando@gmail.com>"
ENV DEBIAN_FRONTEND noninteractive
ENV TZ=Africa/Nairobi
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN apt-get update && apt-get install -y --no-install-recommends \
nano
# Setup flask application
ADD . /home/ubuntu/kycone
RUN  pip install -r /home/ubuntu/kycone/requirements.txt
WORKDIR /home/ubuntu/kycone

#RUN python manage.py db upgrade
# 
EXPOSE 5000



