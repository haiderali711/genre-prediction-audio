# Base Image
FROM continuumio/conda-ci-linux-64-python3.8:latest

USER root 

# set default environment variables
ENV PYTHONUNBUFFERED 1 
ENV LANG C.UTF-8

# Upgrade base image
#RUN apt-get update \
#  && apt-get install -y build-essential \
#  wget \
#  unzip \
#  bzip2 \
#  software-properties-common \
#  python-setuptools \
#	python3-venv \
# python3-pip

# Music libraries
#RUN apt-get install -y libasound-dev \
#   portaudio19-dev \
#   libportaudio2 \
#   libportaudiocpp0 \
#   ffmpeg \
#   libavcodec-extra


RUN pip install -U pip


# create and set working directory
ADD . /opt/sources
WORKDIR /opt/sources

RUN conda install -y numba llvmlite \
	asgiref certifi cycler \
	django=3.1.3 joblib kiwisolver \
	matplotlib numpy olefile \
	pandas Pillow pyparsing \
	python-dateutil pytz scikit-learn \
	scipy six sqlparse \
	threadpoolctl tornado gunicorn sip

RUN conda install -c conda-forge librosa

RUN conda update --all

#RUN pip3 install --no-cache-dir -r requirements.txt

WORKDIR /opt/sources/genre_classification

RUN python3 manage.py makemigrations

RUN python3 manage.py migrate

# Expose ports
EXPOSE 8000

ENTRYPOINT ["/bin/bash", "-c", "gunicorn genre_classification.wsgi:application --bind 0.0.0.0:8000 --workers 3"]


