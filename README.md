

# eRCaGuy_PyTerm
A serial terminal/console written in Python. It is a 2-way serial terminal, _with datalogging_. I use it to communicate with Arduinos and other microcontrollers, and log data from them. I like it. 

(I hope to extend it to function with Telnet and possibly other protocols even, later.)

By Gabriel Staples  
www.ElectricRCAircraftGuy.com  


# Status

Ready for use! It works quite well! 


# Dependencies

Install the [pySerial (imported via `import serial`)](https://pypi.org/project/pyserial/) module using pip:

```bash
# Install command for both Linux *and* Windows!
pip3 install pyserial
```

References:
1. pySerial:
    1. https://pypi.org/project/pyserial/
    1. https://pythonhosted.org/pyserial/


# Setup

This program is tested and works on both Linux and Windows. 

If on Windows, however, here are some helpful links and install steps you'll need to do to get a Linux-like environment on Windows so you can run this better:

1. Install Git For Windows to get the Git Bash terminal. Be sure to choose the installation step to add it to the Windows Terminal. See my instructions here:
    1. https://github.com/ElectricRCAircraftGuy/eRCaGuy_dotfiles/issues/27#issue-1950880578
    1. https://stackoverflow.com/a/76950661/4561887
1. Configure your Git Bash home (`~`) directory: 
    1. https://stackoverflow.com/a/77450145/4561887
1. Install Python: 
    1. https://www.python.org/downloads/
1. Set up Python to be runnable inside the Git Bash terminal:
    1. My answer: [Python not working in the command line of git bash](https://stackoverflow.com/a/76918262/4561887)


# Usage

First set all your serial and other parameters inside the `user_config.py` file. Be sure to set `REAL_SERIAL = True`. Optionally turn data-logging on using the appropriate variable, and set your serial port and baudrate in this file.

Then, run `python3 serial_terminal.py` or `./serial_terminal.sh` to run the program. It works quite well. 


# TODO

1. [ ] Post some examples.


# Related

1. [my answer on how to do this in a non-blocking way] [StackOverflow: PySerial non-blocking read loop](https://stackoverflow.com/a/38758773/4561887)
1. [my answer on how to do this in a non-blocking way] [How to read keyboard-input?](https://stackoverflow.com/a/53344690/4561887)
1. [my answer] [Arduino Stack Exchange: Terminal read-only serial monitor without blocking serial port for sketch upload](https://arduino.stackexchange.com/a/78512/7727)
