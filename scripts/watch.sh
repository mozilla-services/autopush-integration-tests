source config.sh

URL_STATUS="https://$HOST_UPDATES/status"
clear; 
JSON=`curl -s "$URL_STATUS"`
VERS_OLD=`echo $JSON | /usr/local/bin/jq '.version' ;` 
say -v "Daniel" $VERS_OLD

while :; do 
   clear; 
   JSON=`curl -s "$URL_STATUS"`
   VERS=`echo $JSON | /usr/local/bin/jq '.version' ; sleep 5;` 
   if [ "$VERS_OLD" == "$VERS" ]; then
      MSG="still same version: $VERS"
      FLAG=0
   else
      MSG="Attention! Attention! Attention! Attention! DNS has changed! New release version is: $VERS"
      FLAG=1
   fi
   echo $MSG 
   say -v "Daniel" $MSG
   if [ $FLAG == 1 ]; then
        echo $MSG 
        break;
   fi
echo $MSG 
say -v "Daniel" $MSG

done
