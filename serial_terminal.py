"""
serial_terminal.py

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

To run this program: `python3 serial_terminal.py`
- See the README for more sophisticated symbolic link solutions which allow you to simply call `serial_terminal`, 
  for instance, instead.

"""

# Internal Modules
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
        self.terminal_prompt_str = 'PyTerm> '
        self.tp_spaces = ' '*len(self.terminal_prompt_str) # Terminal Prompt spaces string
        
        # Obtain location of the user configuration module/file path so we can print it to the user,
        # showing them where it is to modify it.
        # - Source: Retrieving python module path: https://stackoverflow.com/a/12154601/4561887
        self.user_config_path = inspect.getfile(user_config)

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
        
        # Append self.terminal_prompt_str to front of first element in tuple, rebuilding the tuple.
        if (len(args_tuple) > 1):
            args_tuple = (self.terminal_prompt_str + args_tuple[0], args_tuple[1:])
        else:
            args_tuple = (self.terminal_prompt_str + args_tuple[0],)
    
        print(*args_tuple, **kwargs_dict)
    
    def read_kbd_input(self, inputQueue, threadEvent):
        "Stand-alone thread to read (and block on) keyboard inputs."
    
        # Wait here until the other thread calls "threadEvent.set()"
        threadEvent.wait()
        threadEvent.clear()
    
        self.printt('Ready for keyboard input. To exit the serial terminal, type "{}".'.format(user_config.EXIT_COMMAND))
        while (True):
            # Receive keyboard input from user.
            input_str = input()
            
            # Enqueue this input string.
            # Note: Lock not required here since we are only calling a single Queue method, not a sequence of them 
            # which would otherwise need locks to be treated as one atomic operation.
            inputQueue.put(input_str)
    
    def main(self):
        "Main program thread (with infinite loop) to read and process serial data & user commands."
    
        # # Open file for logging
        # if (self.logging_on):
        #     # Get a filename, in desired format. 
        #     # See: https://stackoverflow.com/a/32490661/4561887 and http://strftime.org/
        #     filename = datetime.datetime.today().strftime('%Y%m%d-%H%Mhrs%Ssec_serialdata.txt')
        #     path = user_config.LOG_FOLDER + filename
        #     file = open(path, "w")
        #     self.printt(('Logging all incoming serial messages to\n' + 
        #                  self.tp_spaces + '"{}".').format(path))
    
        self.printt('Using user configuration file: \n' +
                    self.tp_spaces + '"{}".'.format(self.user_config_path))
    
        self.printt(
            ('Opening serial port using PySerial.\n' + 
             self.tp_spaces + 'PySerial serial.Version = {}\n' + 
             self.tp_spaces + 'port = "{}"\n' + 
             self.tp_spaces + 'baudrate = {}\n' +
             self.tp_spaces + 'bytesize = {}\n' + 
             self.tp_spaces + 'parity = {}\n' + 
             self.tp_spaces + 'stopbits = {}\n' + 
             self.tp_spaces + '(read) timeout = {}\n' + 
             self.tp_spaces + 'write_timeout = {}'
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
    
        # Open serial port
        if (user_config.SIMULATE_SERIAL):
            self.printt("SIMULATED SERIAL: ")
    
        if (not user_config.SIMULATE_SERIAL):
            # Open up an actual serial port.
            # - Note: The port is immediately opened (via `open()`) on object creation when a port is given. See:
            # https://pyserial.readthedocs.io/en/latest/pyserial_api.html.
            try:
                ser = serial.Serial(**user_config.serial_config)
            except serial.serialutil.SerialException as e:
                self.printt("FAILED SERIAL OBJECT CREATION: Plug in your serial device.\n" +
                            self.tp_spaces + repr(e))
                return
    
        # NOT NEEDED YET: To enforce atomic access to a chunk of multiple queue method calls in a row.
        # queueLock = threading.Lock() 
        
        #Keyboard input queue
        inputQueue = queue.Queue()
    
        # For synchronizing threads.
        threadEvent = threading.Event()
    
        # Create & start a thread to read keyboard input.
        # Set daemon to True to auto-kill this thread when all other non-daemonic threads are exited. This is desired since
        # this thread has no cleanup to do, which would otherwise require a more graceful approach to clean up then exit.
        inputThread = threading.Thread(target=self.read_kbd_input, args=(inputQueue, threadEvent), daemon=True)
        inputThread.start()
    

#########################
#             file.write('Serial settings:\n'#############
#                        '  port = {}\n'
#                        '  baudrate = {}\n'
#                        '  parity = {}\n'
#                        '  stopbits = {}\n'
#                        '  bytesize = {}\n'.format(port, baudrate, serial.PARITY_NONE, serial.STOPBITS_ONE, 
#                                                   serial.EIGHTBITS)
#                       )
    
        # Don't let the inputThread continue until we are ready to start the main loop. Let it continue now.
        threadEvent.set()
    
        # main loop
        while (True):
            # Read incoming serial data
            if (not user_config.SIMULATE_SERIAL):
                if (ser.inWaiting() > 0):
                    # Print as ascii-decoded data:
                    data_str = ser.read(ser.inWaiting()).decode('ascii')
                    print(data_str, end='') 
    
                    # # OR: print as binary data that has been converted to a string-representable format 
                    # # (ex: make \n and \r printable):
                    # data_str = repr(ser.read(ser.inWaiting()))
                    # print(data_str) 
    
                    if (self.logging_on):
                        file.write(data_str)
                        file.flush() # Force immediate write to file instead of buffering
            
            # Read keyboard inputs
            # Note: if this queue were being read in multiple places we would need to use locks to ensure multi-method-call
            # atomic access. Since this is the only place we can remove from the queue, however, no locks are required.
            if (inputQueue.qsize() > 0):
                input_str = inputQueue.get()
                # self.printt("input_str = {}".format(input_str))
    
                if (input_str == user_config.EXIT_COMMAND):
                    self.printt("Exiting serial terminal.")
                    break
                # TODO: add the ability to read in arrow keys (ex: up arrow to show the last command)
                # This may take a bit of effort, as the below code does not work.
                # elif (input_str == "^[[A"):
                #     self.printt("You pressed Up.")
                
                if (not user_config.SIMULATE_SERIAL):
                    input_str += user_config.terminating_chars
                    input_str_encoded = input_str.encode('ascii')
                    ser.write(input_str_encoded)
    
            # Sleep for a short time to prevent this thread from sucking up all of your CPU resources on your PC.
            time.sleep(0.01) 
    
        # Cleanup before quitting
        ########### TODO: ADD THIS AS PART OF THE TRY EXCEPT TYPE ERROR CHECKING CODE SO IT WILL CALL THIS EVERY 
        # TIME THERE IS ANY TYPE OF MAJOR FAILURE WHICH CAUSES THE PROGRAM TO ABORT
        if (not user_config.SIMULATE_SERIAL):
            ser.close()
        if (self.logging_on):
            file.close()
        
        self.printt("End.")
    
    def parseArgs(self):
    
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
    
        self.help_str = (
            'Command syntax: `serial_terminal [serial_port] [baudrate]`\n'
            'Examples:\n'
            '  `serial_terminal`\n'
            '  `serial_terminal /dev/ttyUSB1`\n'
            '  `serial_terminal /dev/ttyUSB1 115200`\n'
            'To change other settings, or user configuration defaults, edit the user configuration file directly, '
            'here:\n'
            '  "{}"'.format(self.user_config_path)
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
    "main function"
    term = Terminal()
    parseArgsErr = term.parseArgs()
    if (parseArgsErr == ParseArgsErr.OK):
        term.main()

if (__name__ == '__main__'):
    main()

