#!/bin/bash
set -x

# Rip environement
#. ~/machinekit/scripts/rip-environment

export DEBUG=5

# make msgd builtin webserver to respond on 192.168.7.1
#export MSGD_OPTS="--wsdebug 255 --wwwdir /home/machinekit/machinekit/src/rtapi/www"
export MSGD_OPTS="--wsdebug 15 --wwwdir $EMC2_HOME/src/rtapi/www"

# if halscope should connect via X somewhere else, say so here:
#export DISPLAY=1.2.3.4:0.0
#mah: export DISPLAY=193.228.47.195:0.0

# kill any current sessions
realtime stop

# this will leave a halcmd prompt - to check status etc
# to exit the demo just hit ^D

python $EMC2_HOME/src/machinetalk/config-service/configserver.py apps.ini &
CONFIG_SERVER_PID=$!
linuxcnc TCT3D.ini

# cleanup
kill $CONFIG_SERVER_PID

exit 0

