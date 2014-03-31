#!/bin/sh

dtc -O dtb -o BB-LCNC-TCT3D-00A0.dtbo -b 0 -@ BB-LCNC-TCT3D-00A0.dts && \
sudo cp BB-LCNC-TCT3D-00A0.dtbo /lib/firmware/

