#!/bin/bash

source config.sh

echo
echo
echo "------------------------"
echo "[RUN #${counter}]: SCENARIO - LOADTEST"
echo "------------------------"
echo
echo
aplt_testplan wss://$HOST/ "aplt.scenarios:loadtest,1,1,0"
