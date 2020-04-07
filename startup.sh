#!/bin/bash
# 
# rc.local
#
# This script is executed at the end of each multiuser runlevel.
# Make sure that the script will "exit 0" on success or any other
# value on error.
#
# In order to enable or disable this script just change the execution
# bits.
#
# By default this script does nothing.

#加入环境变量
export PYTHONPATH=/home/dcm360/.local/lib/python3.6/site-packages:$PYTHONPATH

/usr/bin/python3 /home/dcm360/object-detection/flask_server.py > /home/dcm360/object-detection/log/test.log &
exit 0
