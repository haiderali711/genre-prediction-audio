# Base Image
FROM python:latest

# set default environment variables
ENV PYTHONUNBUFFERED 1 
ENV LANG C.UTF-8

# Upgrade base image
RUN apt-get update -y && \
    apt-get upgrade -y && \
    apt-get dist-upgrade -y

# create and set working directory
RUN mkdir /app

#add project files to the usr/src/app folder
ADD . /app

WORKDIR /app

RUN pip3 install --no-cache-dir -r requirements.txt

WORKDIR /app/genre_classification

# Expose ports
EXPOSE 8000

# default command to execute    
CMD exec gunicorn genre_classification.wsgi:application --bind 0.0.0.0:8000 --workers 3
