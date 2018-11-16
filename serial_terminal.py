"""
serial_terminal.py

Gabriel Staples
14 Nov. 2018

References:
- https://pyserial.readthedocs.io/en/latest/pyserial_api.html
- *****https://www.tutorialspoint.com/python/python_multithreading.htm
- *****https://en.wikibooks.org/wiki/Python_Programming/Threading
- https://stackoverflow.com/questions/1607612/python-how-do-i-make-a-subclass-from-a-superclass
- https://docs.python.org/3/library/queue.html
- https://docs.python.org/3.7/library/threading.html

To install PySerial: `sudo python3 -m pip install pyserial`

To run this program: `python3 serial_terminal.py`

"""

import queue
import threading
import time
import serial

# Global variables
exitFlag = False # Set to True to cause the program to quit
# For testing purposes, where no serial device is plugged in, set to True
NO_SERIAL = True

def read_kbd_input(inputQueue):
    print('Ready for keyboard input:')
    while (True):
        # Receive keyboard input from user.
        input_str = input()
        
        # Enqueue this input string.
        # Note: Lock not required here since multiple queue methods are not required to be called as a single atomic
        # unit.
        inputQueue.put(input_str)

def main():
    global exitFlag
    global KBD_INPUT_PROMPT

    # Open serial port
    # Note: The port is immediately opened on object creation when a port is given. See:
    # https://pyserial.readthedocs.io/en/latest/pyserial_api.html.
    port = '/dev/ttyUSB1'
    baudrate = 115200

    if (NO_SERIAL == True):
        print("SIMULATED SERIAL: ")

    print('Opening serial port using PySerial. serial.Version = {}\n'
          '  port = "{}", baudrate = {}'.format(serial.VERSION, port, baudrate))

    if (NO_SERIAL == False):
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

    # Create & start a thread to read keyboard input.
    # Set daemon to True to auto-kill this thread when all other non-daemonic threads are exited. This is desired since
    # this thread has no cleanup to do, which would otherwise require a more graceful approach to clean up then exit.
    inputThread = threading.Thread(target=read_kbd_input, args=(inputQueue,), daemon=True)
    inputThread.start()

    while (exitFlag == False):
        # Read incoming serial data
        if (NO_SERIAL == False):
            if (ser.inWaiting() > 0):
                data_str = ser.read(ser.inWaiting()).decode('ascii')
                print(data_str, end='') 
        
        # Read keyboard inputs
        # Note: if this queue were being read in multiple places we would need to use locks to ensure multi-method-call
        # atomic access. Since this is the only place we can remove from the queue, however, no locks are required.
        if (inputQueue.qsize() > 0):
            input_str = inputQueue.get()
            print("input_str = {}".format(input_str))

            if (input_str == 'exit'):
                print("Exiting program.")
                exitFlag = True

        # Sleep for a short time to prevent this thread from sucking up all of your CPU resources on your PC.
        time.sleep(0.01) 

    if (NO_SERIAL == False):
        ser.close()
    
    print("End of program.")

if (__name__ == '__main__'):
    main()