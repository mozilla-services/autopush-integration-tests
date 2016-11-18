#!/bin/bash

source config.sh

counter=0
while true; do
    echo
    echo
    echo "------------------------"
    echo "[RUN #${counter}]: SCENARIO - BASIC"
    echo "------------------------"
    echo
    echo
    aplt_testplan wss://$HOST/ "aplt.scenarios:basic,3,1,0,5"
    sleep 10 
    let counter+=1
done
