FROM python:2-stretch

MAINTAINER Stephen Houser <stephenhouser@gmail.com>

RUN apt-get update && \
	apt-get install -y python-pygame

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "./display.py" ]