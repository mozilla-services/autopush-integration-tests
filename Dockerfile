# based on: https://github.com/SeleniumHQ/docker-selenium/blob/master/Base/Dockerfile
# ubuntu:16.04
FROM selenium/standalone-firefox-debug

USER root

ARG FIREFOX_DOWNLOAD_URL=https://download.mozilla.org/?product=firefox-nightly-latest-ssl&lang=en-US&os=linux64 

RUN apt-get -qqy update && apt-get install -qqy \ 
    git \
    python \
    python-dev \
    python-pip \ 
    build-essential \
    && pip install --upgrade pip \
    && rm -rf /var/lib/apt/lists/* /var/cache/apt/*

RUN pip install --upgrade pip && pip install tox

RUN wget --no-verbose -O /tmp/firefox.tar.bz2 $FIREFOX_DOWNLOAD_URL \
  && rm -rf /opt/firefox \
  && tar -C /opt -xjf /tmp/firefox.tar.bz2 \
  && rm /tmp/firefox.tar.bz2 \
  && mv /opt/firefox /opt/firefox-nightly \
  && ln -fs /opt/firefox-nightly/firefox /usr/bin/firefox

EXPOSE 5900
EXPOSE 4444


WORKDIR /tests
COPY . /tests
RUN pip install -r /tests/requirements/tests.txt

#USER seluser

