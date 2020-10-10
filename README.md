# eRCaGuy_PyTerm
A serial terminal/console written in Python. It is a 2-way serial terminal, _with datalogging_. I use it to communicate with Arduinos and other microcontrollers, and log data from them. I like it. 

(I hope to extend it to function with Telnet and possibly other protocols even, later.)

By Gabriel Staples  
www.ElectricRCAircraftGuy.com  


# Status

Ready for use! It works quite well! 


# Usage

First set all your serial and other parameters inside the `user_config.py` file. Be sure to set `REAL_SERIAL = True`. Optionally turn data-logging on using the appropriate variable, and set your serial port and baudrate in this file.

Then, run `python3 serial_terminal.py` to run the program.  It works quite well. 


# TODO

1. [ ] Post some examples.


# Related:

1. [my answer on how to do this in a non-blocking way] [StackOverflow: PySerial non-blocking read loop](https://stackoverflow.com/a/38758773/4561887)
1. [my answer on how to do this in a non-blocking way] [How to read keyboard-input?](https://stackoverflow.com/a/53344690/4561887)
1. [my answer] [Arduino Stack Exchange: Terminal read-only serial monitor without blocking serial port for sketch upload](https://arduino.stackexchange.com/a/78512/7727)
