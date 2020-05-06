FROM python:3.7-stretch

RUN mkdir /build

WORKDIR /build

ADD . /build

RUN pip install -r requirements.txt

CMD [ "python", "run.py"]
