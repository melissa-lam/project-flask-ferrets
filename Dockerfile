# FROM quay.io/centos/centos:stream8

FROM python:3.9-slim-buster

# RUN dnf install -y python3.9

WORKDIR /myportfolio

COPY requirements.txt

RUN pip3 install -r requirements.txt

COPY . .

CMD ["flask", "run", "--host=0.0.0.0"]

EXPOSE 5000