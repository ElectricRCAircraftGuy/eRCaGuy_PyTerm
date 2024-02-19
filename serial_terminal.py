#!/usr/bin/env python3

"""
serial_terminal.py

Gabriel Staples
Originally Written: 14 Nov. 2018

References:
- https://pyserial.readthedocs.io/en/latest/pyserial_api.html
- *****https://www.tutorialspoint.com/python/python_multithreading.htm
- *****https://en.wikibooks.org/wiki/Python_Programming/Threading
- https://stackoverflow.com/questions/1607612/python-how-do-i-make-a-subclass-from-a-superclass
- https://docs.python.org/3/library/queue.html
- https://docs.python.org/3.7/library/threading.html
- https://docs.python.org/3/library/enum.html

To install PySerial: `sudo python3 -m pip install pyserial`

To run this program: `python3 serial_terminal.py`

"""

# Internal Modules
import user_config as config

# External Modules
import queue
import threading
import time
import serial
import datetime
import sys
import enum
import os
import inspect

# Global variables & "constants"
TERMINAL_PROMPT_STR = "terminal> "
TP_SPACES = ' '*len(TERMINAL_PROMPT_STR) # Terminal Prompt spaces string
user_config_path = 'unk'

# Copied in from user configuration file
REAL_SERIAL = config.REAL_SERIAL
LOGGING_ON = config.LOGGING_ON
LOG_FOLDER = config.LOG_FOLDER
EXIT_COMMAND = config.EXIT_COMMAND
port = config.port
baudrate = config.baudrate 


def print2(*args_tuple, **kwargs_dict):
    """
    Print from terminal

    A print() wrapper to append a short string in front of prints coming from this program itself.
    This helps distinguish data being received over serial from data being printed by this program's internals.
    """

    # Append TERMINAL_PROMPT_STR to front of first element in tuple, rebuilding the tuple
    if (len(args_tuple) > 1):
        args_tuple = (TERMINAL_PROMPT_STR + args_tuple[0], args_tuple[1:])
    else:
        args_tuple = (TERMINAL_PROMPT_STR + args_tuple[0],)

    print(*args_tuple, **kwargs_dict)

def read_kbd_input(inputQueue, threadEvent):
    global EXIT_COMMAND

    # Wait here until the other thread calls "threadEvent.set()"
    threadEvent.wait()
    threadEvent.clear()

    print2('Ready for keyboard input. To exit the serial terminal, type "{}".'.format(EXIT_COMMAND))
    while (True):
        # Receive keyboard input from user.
        input_str = input()
        
        # Enqueue this input string.
        # Note: Lock not required here since we are only calling a single Queue method, not a sequence of them 
        # which would otherwise need to be treated as one atomic operation.
        inputQueue.put(input_str)

def main():
    global EXIT_COMMAND
    global LOG_FOLDER
    global user_config_path

    TERMINATING_CHARS = '\r' # For terminating serial output

    # Open serial port
    # Note: The port is immediately opened on object creation when a port is given. See:
    # https://pyserial.readthedocs.io/en/latest/pyserial_api.html.
    if (REAL_SERIAL == False):
        print2("SIMULATED SERIAL: ")

    print2(('Opening serial port using PySerial.\n' + 
             TP_SPACES + 'PySerial serial.Version = {}\n' + 
             TP_SPACES + 'port = "{}"\n' + 
             TP_SPACES + 'baudrate = {}'
            ).format(serial.VERSION, port, baudrate))

    if (REAL_SERIAL == True):
        ser = serial.Serial(
            port = port, 
            baudrate = baudrate,
            parity = serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            )

    # queueLock = threading.Lock() # To enforce atomic access to a chunk of multiple queue method calls in a row
    #Keyboard input queue
    inputQueue = queue.Queue()

    # For synchronizing threads.
    threadEvent = threading.Event()

    # Create & start a thread to read keyboard input.
    # Set daemon to True to auto-kill this thread when all other non-daemonic threads are exited. This is desired since
    # this thread has no cleanup to do, which would otherwise require a more graceful approach to clean up then exit.
    inputThread = threading.Thread(target=read_kbd_input, args=(inputQueue, threadEvent), daemon=True)
    inputThread.start()

    # File logging
    if (LOGGING_ON == True):
        # Ensure the log folder exists; this is the same as `mkdir -p "$LOG_FOLDER"` in Bash.
        os.makedirs(LOG_FOLDER, exist_ok=True)

        # Get a filename, in desired format. 
        # See: https://stackoverflow.com/a/32490661/4561887 and http://strftime.org/
        filename = datetime.datetime.today().strftime('%Y%m%d-%H%Mhrs%Ssec_serialdata.txt')
        path = LOG_FOLDER + filename
        file = open(path, "w")
        print2(('Logging all incoming serial messages to\n' + 
                 TP_SPACES + '"{}".').format(path))

    # Don't let the inputThread continue until we are ready to start the main loop. Let it continue now.
    threadEvent.set()

    # main loop
    while (True):
        # Read incoming serial data
        if (REAL_SERIAL == True):
            if (ser.inWaiting() > 0):
                # Print as ascii-decoded data:
                data_str = ser.read(ser.inWaiting()).decode('ascii')
                print(data_str, end='') 

                # # OR: print as binary data that has been converted to a string-representable format 
                # # (ex: make \n and \r printable):
                # data_str = repr(ser.read(ser.inWaiting()))
                # print(data_str) 

                if (LOGGING_ON == True):
                    file.write(data_str)
                    file.flush() # Force immediate write to file instead of buffering
        
        # Read keyboard inputs
        # Note: if this queue were being read in multiple places we would need to use locks to ensure multi-method-call
        # atomic access. Since this is the only place we can remove from the queue, however, no locks are required.
        if (inputQueue.qsize() > 0):
            input_str = inputQueue.get()
            # print2("input_str = {}".format(input_str))

            if (input_str == EXIT_COMMAND):
                print2("Exiting serial terminal.")
                break
            # TODO: add the ability to read in arrow keys (ex: up arrow to show the last command)
            # This may take a bit of effort, as the below code does not work.
            # elif (input_str == "^[[A"):
            #     print2("You pressed Up.")
            
            if (REAL_SERIAL == True):
                input_str += TERMINATING_CHARS
                input_str_encoded = input_str.encode('ascii')
                ser.write(input_str_encoded)

        # Sleep for a short time to prevent this thread from sucking up all of your CPU resources on your PC.
        time.sleep(0.01) 

    # Cleanup before quitting
    if (REAL_SERIAL == True):
        ser.close()
    if (LOGGING_ON == True):
        file.close()
    
    print2("End.")

class ParseArgsErr(enum.Enum):
    OK = 0
    EXIT = 1

def parseArgs():
    global port
    global baudrate
    global user_config_path

    parseArgsErr = ParseArgsErr.OK

    # Obtain location of the user configuration path so that the user knows where it is to modify it.
    # Source: Retrieving python module path: https://stackoverflow.com/a/12154601/4561887
    user_config_path = inspect.getfile(config)
    print2('Using User config file path: \n' +
           TP_SPACES + '"{}".'.format(user_config_path))

    # Interpret incoming arguments. Note that sys.argv[0] is the python filename itself.
    # Ex. command: `python3 this_filename.py /dev/ttyUSB1 115200`
    #   len(sys.argv) = 3
    #   sys.argv[0] = "this_filename.py"
    #   sys.argv[1] = "/dev/ttyUSB1"
    #   sys.argv[2] = "115200"
    
    argsLen = len(sys.argv)
    maxArgsLen = 3

    # FOR DEBUGGING
    # # print arguments
    # print("argsLen = " + str(argsLen))
    # print("Arguments list:")
    # for i in range(len(sys.argv)):
    #     print("sys.argv[" + str(i) + "] = " + str(sys.argv[i]))
    # print()

    # help_str = ''

    # Too many args
    if (argsLen > maxArgsLen):
        print("Error: too many arguments.");
    elif (argsLen > 1):
        # Read in the 2nd argument
        # 'h' or '-h'
        if (sys.argv[1] == 'h' or sys.argv[1] == '-h'):
            print('Command syntax: `serial_terminal (optional)<serial_port> (optional)<baudrate>`\n'
                  'Examples:\n'
                  '  `serial_terminal`\n'
                  '  `serial_terminal /dev/ttyUSB1`\n'
                  '  `serial_terminal /dev/ttyUSB1 115200`')
            parseArgsErr = ParseArgsErr.EXIT
        # <serial_port>
        else: 
            port = sys.argv[1]
            # print('port = "{}"'.format(port))
    if (argsLen > 2):
        # Read in 3rd argument
        # <baudrate>
        baudrate = int(sys.argv[2])
        # print('baudrate = {}'.format(baudrate))

    return parseArgsErr

if (__name__ == '__main__'):
    parseArgsErr = parseArgs()
    if (parseArgsErr == ParseArgsErr.OK):
        main()

