#!/bin/bash


PWD=`pwd`

# PROD 
HOST="push.services.mozilla.com"
HOST_UPDATES="updates.push.services.mozilla.com"
TEST_ENV="PROD"

# STAGE 
HOST="autopush.stage.mozaws.net"
HOST_UPDATES="updates-autopush.stage.mozaws.net"
TEST_ENV="STAGE"

# DEV 
#HOST="autopush.dev.mozaws.net"
#HOST_UPDATES="updates-autopush.dev.mozaws.net"
#TEST_ENV="DEV"

# RUN ONCE
RUN_ONCE=1 # True
ATTACK_INSTANCES=1

# ACTIVATE ap-loadtester VIRTUALENV
PATH_AP_LOADTESTER=~/git/ap-loadtester

cd $PATH_AP_LOADTESTER
source apenv/bin/activate
cd $PWD
