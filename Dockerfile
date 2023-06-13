FROM python:3.9

WORKDIR /src
COPY requirements.txt /src
RUN pip3 install -r requirements.txt
COPY . /src
