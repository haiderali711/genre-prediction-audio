
# The build-stage image:
FROM continuumio/miniconda3 AS build

USER root 

# set default environment variables
ENV PYTHONUNBUFFERED 1 
ENV LANG C.UTF-8

#Updating the conda the newer version
RUN conda update -n base -c defaults conda

# Install the package as normal:
COPY environment.yml .
RUN conda env create -f environment.yml


# Install conda-pack:
RUN conda install -c conda-forge conda-pack

# Use conda-pack to create a standalone enviornment
# in /venv:
RUN conda-pack -n example -o /tmp/env.tar && \
	mkdir /venv && cd /venv && tar xf /tmp/env.tar && \
	rm /tmp/env.tar

# We've put venv in same path it'll be in final image,
# so now fix up paths:
RUN /venv/bin/conda-unpack


# The runtime-stage image; we can use Debian as the
# base image since the Conda env also includes Python
# for us.
FROM debian:buster AS runtime

#Choose the root user for Sudo permissions issues
USER root 

# Copy /venv from the previous stage:
COPY --from=build /venv /venv

#Copy everything from the repostory folder to sources folder 
ADD . /opt/sources
WORKDIR /opt/sources/genre_classification

#select the bash shell to execute the coming commands
SHELL ["/bin/bash", "-c"]

# Expose ports
EXPOSE 8000

# Choose the venv environment and execute the migrations 
# for the django project
RUN source /venv/bin/activate && \
	python3 manage.py makemigrations && \
	python3 manage.py migrate


# Start the gunicorn for running the application server

ENTRYPOINT source /venv/bin/activate && \
	gunicorn genre_classification.wsgi:application --bind 0.0.0.0:8000 --workers 3
