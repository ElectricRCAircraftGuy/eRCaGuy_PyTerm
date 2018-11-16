#!/bin/sh

# GS
# 16 Nov. 2018 

# Be sure to forward the incoming arguments on to the python script using the `"$@"` part. See: https://stackoverflow.com/a/14340879/4561887
python3 /home/gabriels/GS/dev/Python/Projects/serial_terminal/serial_terminal.py "$@"
