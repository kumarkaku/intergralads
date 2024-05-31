FROM alpine:3.10.3

USER root
ENV PYTHONUNBUFFERED=1
RUN apk add --update --no-cache python3 && ln -sf python3 /usr/bin/python
RUN python3 -m ensurepip
RUN pip3 install --no-cache --upgrade pip setuptools
RUN mkdir /app
COPY yLHuntington.py /app
WORKDIR /app
CMD python yLHuntington.py


