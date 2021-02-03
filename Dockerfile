# https://hub.docker.com/_/python

from python:3.9.1

WORKDIR /Users/electronhead/dev/pyrambium/

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY ./base .
COPY ./app .
COPY ./addendum .

CMD [ "python", "./app/main.py"]