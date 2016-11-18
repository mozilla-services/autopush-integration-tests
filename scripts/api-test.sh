#!/bin/bash

source config.sh

counter=0
while true; do
    echo
    echo
    echo "------------------------"
    echo "[RUN #${counter}]: SCENARIO - API_TEST"
    echo "------------------------"
    echo
    echo
    aplt_testplan wss://push.services.mozilla.com/ "aplt.scenarios:api_test,1,1,0"
    sleep 15 
    let counter+=1
done
