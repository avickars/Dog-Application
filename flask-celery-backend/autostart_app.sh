#!/bin/bash

processId=$(ps -ef | grep 'app.py' | grep -v 'grep' | awk '{ printf $2 }')
echo $processId
if [ $processId ]
then
   echo "Application running"
else
   echo "Application not running"
   cd /home/ubuntu/Dog-Application/flask-celery-backend
   source venv/bin/activate
   python app.py &
   echo "Application started now"
fi
