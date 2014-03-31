#!/bin/bash

dtbo_err () {
	echo "Error loading device tree overlay file: $DTBO" >&2
	exit 1
}

pin_err () {
	echo "Error exporting pin:$PIN" >&2
	exit 1
}

dir_err () {
	echo "Error setting direction:$DIR on pin:$PIN" >&2
	exit 1
}

SLOTS=/sys/devices/bone_capemgr.*/slots

# Make sure required device tree overlay(s) are loaded
# cape-bone-iio
for DTBO in BB-LCNC-TCT3D ; do

	if grep -q $DTBO $SLOTS ; then
		echo $DTBO overlay found
	else
		echo Loading $DTBO overlay
		sudo -A su -c "echo $DTBO > $SLOTS" || dtbo_err
		sleep 1
	fi
done;

if [ ! -r /dev/i2c-2 ] ; then
	echo IC2 device file not found in /dev/i2c-2 >&2
	exit 1;
fi

if [ ! -r /sys/class/uio/uio0 ] ; then
	echo PRU control files not found in /sys/class/uio/uio0 >&2
	exit 1;
fi

# Export GPIO pins:
# One pin needs to be exported to enable the low-level clocks for the GPIO
# modules (there is probably a better way to do this)
# 
# Any GPIO pins driven by the PRU need to have their direction set properly
# here.  The PRU does not do any setup of the GPIO, it just yanks on the
# pins and assumes you have the output enables configured already
# 
# Direct PRU inputs and outputs do not need to be configured here, the pin
# mux setup (which is handled by the device tree overlay) should be all
# the setup needed.
# 
# Any GPIO pins driven by the hal_bb_gpio driver do not need to be
# configured here.  The hal_bb_gpio module handles setting the output
# enable bits properly.  These pins _can_ however be set here without
# causing problems.  You may wish to do this for documentation or to make
# sure the pin starts with a known value as soon as possible.

while read PIN DIR JUNK ; do
        case "$PIN" in
        ""|\#*)	
		continue ;;
        *)
		[ -r /sys/class/gpio/gpio$PIN ] && continue
                sudo -A su -c "echo $PIN > /sys/class/gpio/export" || pin_err
		sudo -A su -c "echo $DIR > /sys/class/gpio/gpio$PIN/direction" || dir_err
                ;;
        esac

done <<- EOF
	66	out 	# P8.7		gpio2.2		Machine_Pwr
	45	out	# P8.11		gpio1.13	X_Dir
	44	out	# P8.12		gpio1.12	X_Step
	47	out	# P8.15		gpio1.15	Y_Dir
	46	out	# P8.16		gpio1.14	Y_Step
	22	out	# P8.19		gpio0.22	Estop_Sw
	61	out	# P8.26		gpio1.29	Status
	30	out	# P9.11		gpio0.30	B_Step
	31	out	# P9.13		gpio0.31	Z_Step
	3	out	# P9.21		gpio0.3		A_Dir
	2	out	# P9.22		gpio0.2		A_Step
	117	out	# P9.25		gpio3.21	Z_Dir
	20	in	# P9.41		gpio0.20	Estop_Ext
	7	out	# P9.42		gpio0.7		B_Dir
EOF