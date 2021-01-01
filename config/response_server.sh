REACT_PID=$(pgrep -f reactions)
#echo $REACT_PID

if [[ ! -z "$REACT_PID" ]]; then
  kill -9 $REACT_PID
fi

nohup python -m rasa_core_sdk.endpoint --actions domain.scheduler.reactions & echo $!
