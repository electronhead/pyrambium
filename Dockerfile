# https://hub.docker.com/_/python

FROM python:3.9.1

WORKDIR /Users/electronhead/dev/pyrambium/

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY app .
COPY mothership .

CMD [ "python", "app/main.py"]