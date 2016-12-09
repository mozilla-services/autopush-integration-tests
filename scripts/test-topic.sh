#!/bin/bash

clear

source ./venv/bin/activate
TOPIC=sometopic
TTL=360
MAX=5
for msg in {1..5}; do
    topic_pusher --ttl $TTL --msg some_msg_here_$msg --topic $TOPIC
done
