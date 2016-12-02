#!/bin/bash

source config.sh

scenarios=(
  "aplt.scenarios:basic,10,1,0"
  "aplt.scenarios:notification_forever_stored,$ATTACK_INSTANCES,1,0,3,360,30,30,$RUN_ONCE"
  "aplt.scenarios:notification_forever_unsubscribed,$ATTACK_INSTANCES,1,0,1,$RUN_ONCE"
  "aplt.scenarios:notification_forever_bad_tokens,$ATTACK_INSTANCES,1,0,1,$RUN_ONCE"
  "aplt.scenarios:notification_forever_bad_endpoints,$ATTACK_INSTANCES,1,0,1,$RUN_ONCE"
)

echo
echo "========================================================="
echo "$HOST"
echo "========================================================="

for CMD in "${scenarios[@]}"
do
    echo
    echo
    echo "--------------------------------------------"
    echo "RUN: SCENARIO - $CMD"
    echo "--------------------------------------------"
    aplt_testplan wss://$HOST/ $CMD
    echo
    echo
done
