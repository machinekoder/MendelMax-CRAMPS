#!/bin/bash
export DEBUG=5

# make msgd builtin webserver to respond on 192.168.7.1
#export MSGD_OPTS="--wsdebug 255 --wwwdir /home/linuxcnc/machinekit/src/rtapi/www"
export MSGD_OPTS="--wsdebug 15 --wwwdir /home/linuxcnc/machinekit/src/rtapi/www"

# if halscope should connect via X somewhere else, say so here:
#export DISPLAY=1.2.3.4:0.0
#mah: export DISPLAY=193.228.47.195:0.0

. /home/linuxcnc/machinekit/scripts/rip-environment

# kill any current sessions
realtime stop

#cd  /home/linuxcnc/machinekit/src/hal/haltalk/examples

# this will leave a halcmd prompt - to check status etc
# to exit the demo just hit ^D

python /home/linuxcnc/machinekit/src/middleware/config-service/configserver.py &
linuxcnc TCT3D.ini

exit 0

