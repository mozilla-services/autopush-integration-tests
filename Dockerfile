FROM frolvlad/alpine-python3

RUN apk add --update git python3-dev

COPY . /app

WORKDIR /app

RUN pip install tox

CMD tox -e $TEST_ENV 
