#!/bin/bash

source config.sh

RUN_ONCE=$1


function run_scenario() {
    echo
    echo
    echo "------------------------"
    echo "[RUN #${counter}]: SCENARIO - BASIC"
    echo "------------------------"
    echo
    echo
    aplt_testplan wss://$HOST/ "aplt.scenarios:basic,3,1,0"
    echo
}

counter=0
if [[ -z $RUN_ONCE ]]; then 
    while true; do
	run_scenario
	sleep 10 
	let counter+=1
    done
else
    run_scenario
fi
