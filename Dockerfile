FROM python:3.7-slim-buster

MAINTAINER Gonzalo Munoz "gonzaloan.munoz@gmail.com"

# Copy file of requirements to image and install dependencies
COPY ./requirements.txt /requirements.txt

RUN apt-get update
RUN pip install -r /requirements.txt


# copy app folder
RUN mkdir /app
WORKDIR /app
COPY . /app

EXPOSE 5000
CMD ["python", "run.py"]