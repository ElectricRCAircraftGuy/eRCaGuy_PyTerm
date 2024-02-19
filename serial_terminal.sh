#!/usr/bin/env bash

# GS
# 16 Nov. 2018 

# See: https://stackoverflow.com/a/60157372/4561887
FULL_PATH_TO_SCRIPT="$(realpath "${BASH_SOURCE[-1]}")"
SCRIPT_DIRECTORY="$(dirname "$FULL_PATH_TO_SCRIPT")"
SCRIPT_FILENAME="$(basename "$FULL_PATH_TO_SCRIPT")"

cd "$SCRIPT_DIRECTORY"

# Be sure to forward the incoming arguments on to the python script using the `"$@"` part. See: https://stackoverflow.com/a/14340879/4561887
python3 serial_terminal.py "$@"

