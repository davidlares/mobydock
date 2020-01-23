FROM python:2.7.10-slim
MAINTAINER David E Lares <david.e.lares@gmail.com>
# installing environment
RUN apt-get update && apt-get install -qq -y build-essential libpq-dev postgresql-client-9.4 --fix-missing --no-install-recommends
# setting the installation path
ENV INSTALL_PATH /mobydock
RUN mkdir -p $INSTALL_PATH
# setting the working directory
WORKDIR $INSTALL_PATH
# copying file dependencies
COPY requirements.txt requirements.txt
# installing app requirements
RUN pip install -r requirements.txt
# copying app folder directories to the container
COPY . .
# static volume for files (served by nginx)
VOLUME ['static']
# serving the app  address
CMD gunicorn -b 0.0.0.0:8000 "mobydock.app:create_app()"
