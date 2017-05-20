# load env vars
include test_env.conf
export $(shell sed 's/=.*//' test_env.conf)

PYTHON = python2
PIP = pip
INSTALL = $(PIP) install


.PHONY: all install build
.PHONY: docker-build docker-run docker-export
.PHONY: test 
.PHONY: clean clean-env

all: build

install:
	$(INSTALL) tox 

build: install

test: 
	bash -c "URL_SERVERS=$(URL_SERVERS) GITHUB_ACCESS_TOKEN=$(GITHUB_ACCESS_TOKEN) tox -e $(TEST_ENV)"

docker-build:
	docker build -t firefoxtesteng/$(PROJECT)-$(TEST_TYPE)-tests .

docker-run:
	bash -c "docker run -e TEST_ENV=$(TEST_ENV) -e GITHUB_ACCESS_TOKEN=$(GITHUB_ACCESS_TOKEN) firefoxtesteng/$(PROJECT)-$(TEST_TYPE)-tests"

docker-test: docker-run

docker-push:
	docker push "firefoxtesteng/$(PROJECT)-$(TEST_TYPE)-tests:latest"

docker-tag:
	docker tag "firefoxtesteng/$(PROJECT)-$(TEST_TYPE)-tests" "firefoxtesteng/$(PROJECT)-$(TEST_TYPE)-tests:latest"

docker-export:
	docker save "firefoxtesteng/$(PROJECT)-$(TEST_TYPE)-tests:latest" | bzip2> "$(PROJECT)-$(TEST_TYPE)-tests.tar.bz2"


clean: 
	@rm -fr venv/ __pycache__/ 

clean-env:
	@cp test_env.conf test_env.conf.OLD
	@rm -f test_env.conf
	@touch test_env.conf

