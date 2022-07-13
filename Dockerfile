# FROM quay.io/centos/centos:stream8

#size of overall image is as small as possible
FROM python:3.9-slim-buster

# RUN dnf install -y python3.9

#specifying /myportfolio as working directory of container image
WORKDIR /myportfolio

#improves layer caching by having two COPY
COPY requirements.txt .

RUN pip3 install -r requirements.txt

#copy all project files into the container image at the working directory
COPY . .

#specify command that runs when a container is created from this container image
CMD ["flask", "run", "--host=0.0.0.0"]

#specify port that will be exposed from the container
EXPOSE 5000