# eRCaGuy_PyTerm
A serial terminal/console written in Python (I hope to extend it to Telnet and others later)

*Note: the `.project` and `.pydevproject` files are the Eclipse-based PyDev project files I use to open this project in Eclipse. Feel free to delete them and/or recreate them yourself by creating your own PyDev (Eclipse) project from this source code.*

This tool can act as a nice replacement for the Arduino Serial Monitor, by the way, and does automatic live data-logging of all data coming in over serial. This is useful if you want to record a serial data stream coming in from a serial device, such as an Arduino, for data collection and post-analysis. This could also be really useful in laboratory research in universities by researchers/professors/students, and other engineers.

# Requires:

python3  
[pySerial](https://pyserial.readthedocs.io/en/latest/pyserial_api.html)

# Instructions:

## Linux:
Create a symbolic link in your Linux home directory so you can run this program simply by calling `serial_terminal` from any directory in the terminal. Be sure to use the full path to the .sh shell script:

(RECOMMENDED) "Install" (ie: to run via a symbolic link in your user bin directory):

    mkdir -p ~/bin && ln -s full/path/to/serial_terminal.sh ~/bin/serial_terminal

Run without install:

If you skip this step you can still run it by calling the full path to `serial_terminal.sh` or by using the full path to the .py file in this direct python call: `python3 serial_terminal.py`.

See all plugged in serial USB devices:

    ls /dev/ttyUSB*

## Windows:

To Run:

Use `py -3 serial_terminal.py` in the commands below, rather than `serial_terminal` or `python3 serial_terminal.py`.


## User settings can be edited directly in `user_config.py`.

## Commands:

Replace `serial_terminal` with the proper command, as described above in the "Linux" and "Windows" sections.

For help:

    serial_terminal -h

Command syntax: 

    serial_terminal [serial_port] [baudrate]

Sample commands to run this program:

    serial_terminal
    serial_terminal /dev/ttyUSB1
    serial_terminal /dev/ttyUSB1 115200

