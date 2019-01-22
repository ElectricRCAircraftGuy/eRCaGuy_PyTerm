"""
pyterm.py (was serial_terminal.py)

Gabriel Staples
Website: www.ElectricRCAircraftGuy.com
- click "Feedback/Corrections/Contact me" link at top of website to get my email
Project page: https://github.com/ElectricRCAircraftGuy/eRCaGuy_PyTerm
Started: 14 Nov. 2018

References:
1. PySerial (Python serial library) documentation: https://pyserial.readthedocs.io/en/latest/pyserial_api.html
2. *****https://www.tutorialspoint.com/python/python_multithreading.htm
3. *****https://en.wikibooks.org/wiki/Python_Programming/Threading
4. https://stackoverflow.com/questions/1607612/python-how-do-i-make-a-subclass-from-a-superclass
5. https://docs.python.org/3/library/queue.html
6. https://docs.python.org/3.7/library/threading.html
7. https://docs.python.org/3/library/enum.html
8. https://en.wikipedia.org/wiki/8-N-1 
9. https://stackoverflow.com/questions/4308182/getting-the-exception-value-in-python

To install PySerial: `sudo python3 -m pip install pyserial`

To run this program: `python3 pyterm.py`
- See the README for more sophisticated symbolic link solutions which allow you to simply call `pyterm`, 
  for instance, instead.

"""

# Internal Modules
import logger
import user_config

# External Modules
import datetime
import enum
import inspect # find the path to a module
import os
import queue
import serial
import sys
import threading
import time

class ParseArgsErr(enum.Enum):
    """
    Error code enum for parsing command-line input arguments to this program.
    - Note: This is a custom enum child class which inherits from parent class enum.Enum.
    """
    # Shared class members
    OK = 0
    EXIT = 1

class Terminal():
    "Class to talk to a device via a (serial) terminal"

    # Shared class members:
    # (None)
    
    def __init__(self):
        "Class constructor."
        # Terminal prompt string to indicate messages being printed by this application, as opposed to messages
        # coming in over serial
        self.prompt_str = 'PyTerm> ' 
        self.tp_spaces = ' '*len(self.prompt_str) # Terminal Prompt spaces string
        
        # Open file for logging
        self.logger = logger.Logger(self.printt, self.tp_spaces)
    
        self.logger.log('Using user configuration file: \n' +
                        self.tp_spaces + '"{}".\n'.format(user_config.user_config_path))
    
        # Open serial port:
        
        self.ser = None
        self.logger.log(
            ('Opening serial port using PySerial.\n' + 
             self.tp_spaces + 'PySerial serial.Version = {}\n' + 
             self.tp_spaces + 'port = "{}"\n' + 
             self.tp_spaces + 'baudrate = {}\n' +
             self.tp_spaces + 'bytesize = {}\n' + 
             self.tp_spaces + 'parity = {}\n' + 
             self.tp_spaces + 'stopbits = {}\n' + 
             self.tp_spaces + '(read) timeout = {}\n' + 
             self.tp_spaces + 'write_timeout = {}\n'
             ).format(
                 serial.VERSION, 
                 user_config.serial_config['port'], 
                 user_config.serial_config['baudrate'], 
                 user_config.serial_config['bytesize'], 
                 user_config.serial_config['parity'], 
                 user_config.serial_config['stopbits'], 
                 user_config.serial_config['timeout'], 
                 user_config.serial_config['write_timeout'], 
             )
        )
        
        # Simulated serial (don't try to open up a serial port)
        if (user_config.SIMULATE_SERIAL):
            self.logger.log("SIMULATED SERIAL: \n")
        # Actual serial
        else:
            # Open up an actual serial port.
            # - Note: The port is immediately opened (via `open()`) on object creation when a port is given. See:
            # https://pyserial.readthedocs.io/en/latest/pyserial_api.html.
            try:
                self.ser = serial.Serial(**user_config.serial_config)
            except serial.serialutil.SerialException as e:
                self.logger.log("FAILED SERIAL OBJECT CREATION: Plug in your serial device and/or make sure it's " + 
                                "not busy!\n" + 
                                self.tp_spaces + repr(e) + "\n")
                self.close()
                return
    
        # NOT NEEDED YET: To enforce atomic access to a chunk of multiple queue method calls in a row.
        # queueLock = threading.Lock() 
        
        #Keyboard input queue
        self.inputQueue = queue.Queue()
    
        # For synchronizing threads.
        self.threadEvent = threading.Event()
    
        # Create & start a thread to read keyboard input.
        # Set daemon to True to auto-kill this thread when all other non-daemonic threads are exited. 
        # This is desired since this thread has no cleanup to do, which would otherwise require a more 
        # graceful approach to clean up then exit.
        inputThread = threading.Thread(target=self.read_kbd_input, args=(), daemon=True)
        inputThread.start()
        
        self.main() # Start main loop

    def printt(self, *args_tuple, **kwargs_dict):
        """
        Print from terminal.
    
        A print() wrapper to append a short string in front of prints coming from this program itself.
        This helps distinguish data being received over serial from data being printed by this program's internals.
        
        Here is the print function prototype: `print(*objects, sep=' ', end='\n', file=sys.stdout, flush=False)`.
        - See: https://docs.python.org/3/library/functions.html#print.
        This means that the `args_tuple` contains all objects to print (`*objects`), and the `kwargs_dict` contains
        the `sep`, `end`, `file`, and `flush` parameters.
        """
        
        # Append self.prompt_str to front of first element in tuple, rebuilding the tuple.
        if (len(args_tuple) > 1):
            args_tuple = (self.prompt_str + args_tuple[0], args_tuple[1:])
        else:
            args_tuple = (self.prompt_str + args_tuple[0],)
    
        print(*args_tuple, **kwargs_dict)
    
    def read_kbd_input(self):
        "Stand-alone thread to read (and block on) keyboard inputs."
    
        # Wait here until the other thread calls "threadEvent.set()"
        self.threadEvent.wait()
        self.threadEvent.clear()
    
        self.logger.log('Ready for keyboard input. To exit the serial terminal, type "{}".\n'.format(
                        user_config.EXIT_COMMAND))
        while (True):
            # Receive keyboard input from user.
            input_str = input()
            
            # Enqueue this input string.
            # Note: Lock not required here since we are only calling a single Queue method, not a sequence of them 
            # which would otherwise need locks to be treated as one atomic operation.
            self.inputQueue.put(input_str)
    
    def main(self):
        "Main program thread (with infinite loop) to read and process serial data & user commands."
    
        # Don't let the inputThread continue until we are ready to start the main loop--ie: now.
        self.threadEvent.set()
    
        # main loop
        while (True):
            # 1. Read incoming serial data
            if (not user_config.SIMULATE_SERIAL):
                if (self.ser.inWaiting() > 0):
                    # Print as ascii-decoded data:
                    data_str = self.ser.read(self.ser.inWaiting()).decode('ascii')
                    self.logger.log("ser_data_in> " + data_str)
    
                    # # OR: print as binary data that has been converted to a string-representable format 
                    # # (ex: make \n and \r printable):
                    # data_str = repr(ser.read(ser.inWaiting()))
                    # self.logger.log(data_str) 
            
            # 2. Read keyboard inputs
            # Note: if this queue were being read in multiple places we would need to use locks to 
            # ensure multi-method-call atomic access. Since this is the only place we can remove from
            # the queue, however, no locks are required.
            if (self.inputQueue.qsize() > 0):
                input_str = self.inputQueue.get()
                # self.printt("input_str = {}".format(input_str)) # FOR DEBUGGING
                self.logger.log("kbd_in> " + input_str)
    
                if (input_str == user_config.EXIT_COMMAND):
                    self.logger.log("Exiting serial terminal.\n")
                    break
                
                # TODO: add the ability to read in arrow keys (ex: up arrow to show the last command)
                # This may take a bit of effort, as the below code does not work.
                # elif (input_str == "^[[A"):
                #     self.printt("You pressed Up.")
                
                if (not user_config.SIMULATE_SERIAL):
                    input_str += user_config.line_ending
                    self.logger.log("ser_data_out> " + input_str)
                    input_str_encoded = input_str.encode('ascii')
                    self.ser.write(input_str_encoded)
    
            # Sleep for a short time to prevent this thread from sucking up all of your CPU resources on your PC.
            time.sleep(0.01) 
        
        self.close()
    
    def close(self):
        "Close a Terminal object."

        self.logger.log("Closing Terminal.\n")    
        
        if (self.ser):
            self.ser.close()
        
        self.logger.close()
        
# end of class Terminal()
    
def parseArgs():

    parseArgsErr = ParseArgsErr.OK

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

    help_str = (
        'Command syntax: `serial_terminal [serial_port] [baudrate]`\n'
        'Examples:\n'
        '  `serial_terminal`\n'
        '  `serial_terminal /dev/ttyUSB1`\n'
        '  `serial_terminal /dev/ttyUSB1 115200`\n'
        'To change other settings, or user configuration defaults, edit the user configuration file directly, '
        'here:\n'
        '  "{}"'.format(user_config.user_config_path)
    )

    # Too many args
    if (argsLen > maxArgsLen):
        print("Error: too many arguments.");
        parseArgsErr = ParseArgsErr.EXIT
    elif (argsLen > 1):
        # Read in the 2nd argument
        # 'h' or '-h'
        if (sys.argv[1] == 'h' or sys.argv[1] == '-h'):
            parseArgsErr = ParseArgsErr.EXIT
        # <serial_port>
        else: 
            user_config.serial_config['port'] = sys.argv[1]
            # print('port = "{}"'.format(port))
    
    if (argsLen > 2):
        # Read in 3rd argument
        # <baudrate>
        user_config.serial_config['baudrate'] = int(sys.argv[2])
        # print('baudrate = {}'.format(baudrate))

    if (parseArgsErr != parseArgsErr.OK):
        print(self.help_str)

    return parseArgsErr

def main():
    "Main function."
    
    # Obtain location of the user configuration module/file path so we can print it to the user,
    # showing them where it is to modify it.
    # - Source: Retrieving python module path: https://stackoverflow.com/a/12154601/4561887
    user_config.user_config_path = inspect.getfile(user_config)
    
    parseArgsErr = parseArgs()
    if (parseArgsErr == ParseArgsErr.OK):
        Terminal() # Create a terminal and begin running the main loop
        
    # We will not get to here until the Terminal (object) application has ended.
    print("End of Program")

if (__name__ == '__main__'):
    main()

