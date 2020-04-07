#!/bin/bash
#

#加入环境变量
#export PYTHONPATH=/home/dcm360/.local/lib/python3.6/site-packages:$PYTHONPATH

#/usr/bin/python3 /home/dcm360/object-detection/flask_server.py > /home/dcm360/object-detection/log/test.log &
if test $( pgrep -f 'flask_server' | wc -l ) -eq 0
then
       echo "flask_server is not running, restart"
       export PYTHONPATH=/home/dcm360/.local/lib/python3.6/site-packages:$PYTHONPATH
       /usr/bin/python3 /home/dcm360/object-detection/flask_server.py > /home/dcm360/object-detection/log/test.log &
else
       date >> /home/dcm360/object-detection/test.txt
fi

exit 0
