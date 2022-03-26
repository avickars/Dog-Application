#!/bin/bash

processId=$(ps -ef | grep 'celery -A app.celery worker --loglevel=INFO' | grep -v 'grep' | awk '{ printf $2 }')
echo $processId
if [ $processId ]
then
   echo "celery running"
else
   echo "celery not running"
   cd /home/ubuntu/Dog-Application/flask-celery-backend
   source venv/bin/activate
   celery -A app.celery worker --loglevel=INFO &
   echo "celery started now"
fi
